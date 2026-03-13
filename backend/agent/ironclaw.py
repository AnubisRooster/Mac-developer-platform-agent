"""IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.

IronClaw is a Rust-based OpenClaw runtime that exposes an OpenAI-compatible
gateway API. The Python backend communicates with IronClaw via:

  POST /v1/chat/completions  — prompt interpretation, planning, tool selection
  GET  /v1/models            — health / readiness check

All reasoning is delegated to IronClaw. No reasoning logic is implemented
in Python.
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
    """

    def __init__(self) -> None:
        secrets = get_secrets()
        self._base_url = secrets.ironclaw_url.rstrip("/")
        self._auth_token = secrets.ironclaw_auth_token
        self._timeout = 120.0
        logger.info("IronClawClient initialized: %s", self._base_url)

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

    async def interpret(
        self,
        message: str,
        tools: list[dict[str, Any]],
        context: list[dict[str, str]] | None = None,
        conversation_id: str = "",
    ) -> IronClawResponse:
        """Send a user message to IronClaw for interpretation and task planning.

        Uses the OpenAI-compatible /v1/chat/completions endpoint with
        function-calling tool definitions. IronClaw returns either a
        text response or tool_calls to execute.
        """
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
            "model": "qwen3.5:latest",
            "messages": messages,
        }
        if openai_tools:
            payload["tools"] = openai_tools

        data = await self._post("/v1/chat/completions", payload)

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
        """Delegate content summarization to IronClaw."""
        system_msg = instruction or "Summarize the following content concisely."
        payload = {
            "model": "qwen3.5:latest",
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": content},
            ],
        }
        data = await self._post("/v1/chat/completions", payload)
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

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request to IronClaw and return the JSON response."""
        url = f"{self._base_url}{path}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.debug("POST %s", url)
            resp = await client.post(url, json=payload, headers=self._headers())
            resp.raise_for_status()
            return resp.json()
