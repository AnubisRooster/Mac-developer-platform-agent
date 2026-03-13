"""Conversation memory for maintaining chat history and context."""

from __future__ import annotations

import datetime as dt
import logging
from typing import Any

logger = logging.getLogger("claw-agent.memory")


class ConversationMemory:
    """Stores conversation history for the agent and provides context retrieval."""

    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    def add_message(self, role: str, content: str) -> None:
        self._history.append(
            {
                "role": role,
                "content": content,
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
        )
        logger.debug("Added %s message (%d total)", role, len(self._history))

    def get_context(self, max_messages: int = 20) -> list[dict[str, Any]]:
        return self._history[-max_messages:]

    def get_summary(self) -> str:
        if not self._history:
            return "No messages yet."
        count = len(self._history)
        user_count = sum(1 for m in self._history if m["role"] == "user")
        return f"Conversation: {count} messages ({user_count} from user)."

    def clear(self) -> None:
        self._history.clear()
        logger.info("Conversation memory cleared")

    def to_llm_messages(self) -> list[dict[str, str]]:
        """Return messages in role/content format for IronClaw context."""
        return [{"role": m["role"], "content": m["content"]} for m in self._history]
