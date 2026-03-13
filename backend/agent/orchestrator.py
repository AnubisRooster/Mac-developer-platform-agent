"""Main orchestrator — delegates reasoning to IronClaw, executes tools locally.

The orchestrator coordinates between the IronClaw reasoning engine and
locally-registered Python tool handlers. It never performs prompt
interpretation, task planning, or summarization itself.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from agent.ironclaw import IronClawClient
from agent.memory import ConversationMemory
from database.models import AgentConversation, ToolOutput, get_session
from tools.registry import ToolRegistry

logger = logging.getLogger("claw-agent.orchestrator")


class Orchestrator:
    """Coordinates between IronClaw (reasoning) and tool execution (Python).

    All reasoning — prompt interpretation, task planning, tool selection,
    and summarization — is delegated to IronClaw. The Python orchestrator
    only manages tool execution and persistence.
    """

    def __init__(self) -> None:
        self._ironclaw = IronClawClient()
        self._memory = ConversationMemory()
        self._registry = ToolRegistry()

    @property
    def registry(self) -> ToolRegistry:
        return self._registry

    @property
    def ironclaw(self) -> IronClawClient:
        return self._ironclaw

    def register_tool(
        self,
        name: str,
        func: Any,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """Register a tool in the schema registry."""
        self._registry.register(name, func, description, parameters)

    async def handle_message(
        self,
        user_message: str,
        user_id: str = "",
        channel: str = "",
        conversation_id: str = "",
    ) -> str:
        """Process a user message by delegating reasoning to IronClaw
        and executing the returned action plan locally."""
        self._memory.add_message("user", user_message)
        logger.info("Handling message from user=%s: %s", user_id, user_message[:200])

        tools_for_ironclaw = self._registry.get_all_schemas()
        context = self._memory.to_llm_messages()
        tools_used: list[str] = []

        max_iterations = 10
        for _ in range(max_iterations):
            response = await self._ironclaw.interpret(
                message=user_message,
                tools=tools_for_ironclaw,
                context=context,
                conversation_id=conversation_id,
            )

            if response.type == "response":
                self._memory.add_message("assistant", response.response)
                self._persist_conversation(
                    user_id=user_id,
                    channel=channel,
                    conversation_id=conversation_id,
                    user_message=user_message,
                    agent_response=response.response,
                    tools_used=tools_used,
                )
                return response.response

            for action in response.actions:
                result = await self.execute_tool(action.tool, action.args)
                tools_used.append(action.tool)
                self._memory.add_message(
                    "user", f"[Tool result: {action.tool}]\n{result}"
                )

            context = self._memory.to_llm_messages()

        logger.warning("handle_message hit max iterations (%d)", max_iterations)
        fallback = "I've completed several actions but reached the iteration limit."
        self._memory.add_message("assistant", fallback)
        return fallback

    async def execute_tool(self, tool_name: str, tool_args: dict[str, Any]) -> str:
        """Look up tool, invoke it, persist result, return result string."""
        func = self._registry.get_handler(tool_name)
        if func is None:
            raise KeyError(f"Unknown tool: {tool_name}")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(**tool_args)
            else:
                result = await asyncio.to_thread(func, **tool_args)
        except Exception as e:
            logger.exception("Tool %s failed: %s", tool_name, e)
            result = f"Error: {e}"

        result_str = str(result) if result is not None else ""

        try:
            session = get_session()
            try:
                record = ToolOutput(
                    tool_name=tool_name,
                    input_data=json.dumps(tool_args, default=str),
                    output_data=result_str,
                )
                session.add(record)
                session.commit()
            finally:
                session.close()
        except Exception as e:
            logger.warning("Could not persist ToolOutput: %s", e)

        return result_str

    def _persist_conversation(self, **kwargs: Any) -> None:
        """Store a completed agent conversation in PostgreSQL."""
        try:
            session = get_session()
            try:
                record = AgentConversation(
                    conversation_id=kwargs.get("conversation_id", ""),
                    user_id=kwargs.get("user_id", ""),
                    channel=kwargs.get("channel", ""),
                    user_message=kwargs.get("user_message", ""),
                    agent_response=kwargs.get("agent_response", ""),
                    tools_used=json.dumps(kwargs.get("tools_used", [])),
                )
                session.add(record)
                session.commit()
            finally:
                session.close()
        except Exception as e:
            logger.warning("Could not persist conversation: %s", e)
