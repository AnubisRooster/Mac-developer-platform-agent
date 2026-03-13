"""IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.

IronClaw is a Rust-based OpenClaw runtime that performs:
- Prompt interpretation
- Task planning
- Tool selection
- Summarization

The Python backend communicates with IronClaw exclusively via HTTP.
No reasoning logic is implemented in Python.
"""

from __future__ import annotations

import logging
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

    All prompt interpretation, task planning, tool selection, and
    summarization are delegated to IronClaw over HTTP. The Python
    orchestrator never performs reasoning directly.
    """

    def __init__(self) -> None:
        secrets = get_secrets()
        self._base_url = secrets.ironclaw_url.rstrip("/")
        self._timeout = 120.0
        logger.info("IronClawClient initialized: %s", self._base_url)

    async def interpret(
        self,
        message: str,
        tools: list[dict[str, Any]],
        context: list[dict[str, str]] | None = None,
        conversation_id: str = "",
    ) -> IronClawResponse:
        """Send a user message to IronClaw for interpretation and task planning.

        IronClaw analyzes the message, selects appropriate tools from the
        provided registry, and returns either an action plan to execute
        or a direct text response.
        """
        payload = {
            "message": message,
            "tools": tools,
            "context": context or [],
            "conversation_id": conversation_id,
        }
        data = await self._post("/api/v1/interpret", payload)
        return IronClawResponse(**data)

    async def summarize(self, content: str, instruction: str = "") -> str:
        """Delegate content summarization to IronClaw."""
        payload = {"content": content, "instruction": instruction}
        data = await self._post("/api/v1/summarize", payload)
        return data.get("summary", "")

    async def health(self) -> dict[str, Any]:
        """Check IronClaw runtime health and readiness."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{self._base_url}/health")
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("IronClaw health check failed: %s", e)
            return {"status": "unreachable", "error": str(e)}

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request to IronClaw and return the JSON response."""
        url = f"{self._base_url}{path}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.debug("POST %s", url)
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
