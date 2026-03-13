"""IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.

IronClaw is a Rust-based OpenClaw runtime that exposes an OpenAI-compatible
gateway API. The Python backend communicates with IronClaw via:

  POST /v1/chat/completions  — prompt interpretation, planning, tool selection
  GET  /v1/models            — health / readiness check

All reasoning is delegated to IronClaw. No reasoning logic is implemented
in Python. Supports runtime model switching and OpenRouter cloud fallback.
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

import httpx
from pydantic import BaseModel, Field

from security.secrets import get_secrets

logger = logging.getLogger("claw-agent.ironclaw")

OLLAMA_MODELS = [
    "qwen3.5:latest",
    "llama3.2:latest",
    "gemma3:4b",
    "phi3:3.8b",
]

OPENROUTER_MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
    "google/gemini-pro-1.5",
    "meta-llama/llama-3.1-70b-instruct",
]


class IronClawAction(BaseModel):
    """A single tool action returned by IronClaw's planner."""

    tool: str
    args: dict[str, Any] = Field(default_factory=dict)
    description: str = ""


class IronClawResponse(BaseModel):
    """Structured response from the IronClaw runtime."""

    type: str  # "action_plan" | "response"
    actions: list[IronClawAction] = Field(default_factory=list)
    response: str = ""
    conversation_id: str = ""


class IronClawClient:
    """HTTP client for the IronClaw Rust-based reasoning runtime.

    Communicates via IronClaw's OpenAI-compatible gateway API
    (/v1/chat/completions with tool definitions).
    Supports runtime model switching and OpenRouter cloud fallback.
    """

    def __init__(self) -> None:
        secrets = get_secrets()
        self._base_url = secrets.ironclaw_url.rstrip("/")
        self._auth_token = secrets.ironclaw_auth_token
        self._model = secrets.ironclaw_model
        self._timeout = 120.0

        self._openrouter_api_key = secrets.openrouter_api_key
        self._openrouter_model = secrets.openrouter_model
        self._openrouter_base_url = secrets.openrouter_base_url.rstrip("/")

        self._provider = "ollama"  # "ollama" | "openrouter"
        logger.info("IronClawClient initialized: %s (model=%s)", self._base_url, self._model)

    @property
    def current_model(self) -> str:
        if self._provider == "openrouter":
            return self._openrouter_model
        return self._model

    @property
    def current_provider(self) -> str:
        return self._provider

    def set_model(self, model: str, provider: str = "ollama") -> dict[str, str]:
        """Switch the active model at runtime. Returns the new config."""
        old_model = self.current_model
        old_provider = self._provider
        self._provider = provider
        if provider == "openrouter":
            self._openrouter_model = model
        else:
            self._model = model
        logger.info(
            "Model switched: %s/%s -> %s/%s",
            old_provider, old_model, provider, model,
        )
        return {"provider": provider, "model": model}

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

    def _openrouter_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._openrouter_api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Claw Agent",
        }

    def _completion_url(self) -> tuple[str, dict[str, str]]:
        """Return (url, headers) based on current provider."""
        if self._provider == "openrouter" and self._openrouter_api_key:
            return (
                f"{self._openrouter_base_url}/chat/completions",
                self._openrouter_headers(),
            )
        return (
            f"{self._base_url}/v1/chat/completions",
            self._headers(),
        )

    async def interpret(
        self,
        message: str,
        tools: list[dict[str, Any]],
        context: list[dict[str, str]] | None = None,
        conversation_id: str = "",
    ) -> IronClawResponse:
        """Send a user message for interpretation and task planning."""
        messages: list[dict[str, Any]] = []

        if context:
            for entry in context:
                role = entry.get("role", "user")
                content = entry.get("content", "")
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": message})

        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("parameters", {"type": "object", "properties": {}}),
                },
            }
            for t in tools
        ]

        payload: dict[str, Any] = {
            "model": self.current_model,
            "messages": messages,
        }
        if openai_tools:
            payload["tools"] = openai_tools

        data = await self._completions_post(payload)

        conv_id = conversation_id or data.get("id", str(uuid.uuid4()))
        choices = data.get("choices", [])
        choice = choices[0] if choices else {}
        msg = choice.get("message", {})
        tool_calls = msg.get("tool_calls")

        if tool_calls:
            actions = []
            for tc in tool_calls:
                fn = tc.get("function", {})
                try:
                    args = json.loads(fn.get("arguments", "{}"))
                except (json.JSONDecodeError, TypeError):
                    args = {}
                actions.append(IronClawAction(
                    tool=fn.get("name", ""),
                    args=args,
                    description=f"Tool call {fn.get('name', '')}",
                ))
            return IronClawResponse(
                type="action_plan",
                actions=actions,
                conversation_id=conv_id,
            )

        return IronClawResponse(
            type="response",
            response=msg.get("content", ""),
            conversation_id=conv_id,
        )

    async def summarize(self, content: str, instruction: str = "") -> str:
        """Delegate content summarization."""
        system_msg = instruction or "Summarize the following content concisely."
        payload = {
            "model": self.current_model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": content},
            ],
        }
        data = await self._completions_post(payload)
        choice = data.get("choices", [{}])[0]
        return choice.get("message", {}).get("content", "")

    async def health(self) -> dict[str, Any]:
        """Check IronClaw runtime health by querying /v1/models."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self._base_url}/v1/models",
                    headers=self._headers(),
                )
                resp.raise_for_status()
                data = resp.json()
                models = [m["id"] for m in data.get("data", [])]
                return {"status": "connected", "models": models}
        except Exception as e:
            logger.warning("IronClaw health check failed: %s", e)
            return {
                "status": "unreachable",
                "error": f"IronClaw runtime is not running at {self._base_url} — start it to enable AI reasoning",
            }

    async def test_model(self, model: str, provider: str = "ollama") -> dict[str, Any]:
        """Send a quick test prompt to verify a model is reachable."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say hello in one word."}],
            "max_tokens": 10,
        }
        try:
            if provider == "openrouter" and self._openrouter_api_key:
                url = f"{self._openrouter_base_url}/chat/completions"
                headers = self._openrouter_headers()
            else:
                url = f"{self._base_url}/v1/chat/completions"
                headers = self._headers()

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"ok": True, "model": model, "provider": provider, "response": content}
        except Exception as e:
            logger.warning("Model test failed for %s/%s: %s", provider, model, e)
            return {"ok": False, "model": model, "provider": provider, "error": str(e)}

    async def _completions_post(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a chat completions request using the active provider."""
        url, headers = self._completion_url()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                logger.debug("POST %s (model=%s)", url, payload.get("model"))
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as primary_err:
            if self._provider == "ollama" and self._openrouter_api_key:
                logger.warning(
                    "Ollama request failed (%s), falling back to OpenRouter", primary_err
                )
                fallback_url = f"{self._openrouter_base_url}/chat/completions"
                payload["model"] = self._openrouter_model
                try:
                    async with httpx.AsyncClient(timeout=self._timeout) as client:
                        resp = await client.post(
                            fallback_url, json=payload, headers=self._openrouter_headers()
                        )
                        resp.raise_for_status()
                        return resp.json()
                except Exception as fallback_err:
                    logger.error("OpenRouter fallback also failed: %s", fallback_err)
                    raise fallback_err from primary_err
            raise

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request to IronClaw and return the JSON response."""
        url = f"{self._base_url}{path}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.debug("POST %s", url)
            resp = await client.post(url, json=payload, headers=self._headers())
            resp.raise_for_status()
            return resp.json()
