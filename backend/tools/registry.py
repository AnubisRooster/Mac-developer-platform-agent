"""Tool Schema Registry — integration connectors register tools with schemas.

Each tool includes:
- name: unique identifier (e.g. github.summarize_pr)
- description: human-readable purpose
- parameters: JSON Schema for the tool's arguments
- handler: the Python callable that executes the tool
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from pydantic import BaseModel, Field

logger = logging.getLogger("claw-agent.tools")


class ToolSchema(BaseModel):
    """Public schema for a registered tool, sent to IronClaw and exposed via API."""

    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolEntry:
    """Internal registry entry binding a schema to its handler."""

    __slots__ = ("schema", "handler")

    def __init__(self, schema: ToolSchema, handler: Callable[..., Any]) -> None:
        self.schema = schema
        self.handler = handler


class ToolRegistry:
    """Registry where integration connectors register their tools.

    Provides tool schemas to IronClaw for tool selection and exposes
    the list via the dashboard API.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolEntry] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """Register a tool with its handler and schema."""
        schema = ToolSchema(
            name=name,
            description=description,
            parameters=parameters or {},
        )
        self._tools[name] = ToolEntry(schema=schema, handler=handler)
        logger.debug("Registered tool: %s", name)

    def get_handler(self, name: str) -> Callable[..., Any] | None:
        """Return the callable for the given tool name, or None."""
        entry = self._tools.get(name)
        return entry.handler if entry else None

    def get_schema(self, name: str) -> ToolSchema | None:
        """Return the schema for the given tool name, or None."""
        entry = self._tools.get(name)
        return entry.schema if entry else None

    def list_tools(self) -> list[str]:
        """Return all registered tool names."""
        return list(self._tools.keys())

    def get_all_schemas(self) -> list[dict[str, Any]]:
        """Return all tool schemas as dicts (for IronClaw and API consumers)."""
        return [entry.schema.model_dump() for entry in self._tools.values()]

    def get_tool_descriptions(self) -> str:
        """Return a formatted string of all tool names and descriptions."""
        lines = [
            f"- {e.schema.name}: {e.schema.description}"
            for e in self._tools.values()
        ]
        return "\n".join(lines) if lines else "No tools registered."
