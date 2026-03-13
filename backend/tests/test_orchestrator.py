"""Unit tests for agent.orchestrator.Orchestrator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent.ironclaw import IronClawAction, IronClawResponse


class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_handle_message_direct_response(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            mock_ic = AsyncMock()
            mock_ic.interpret.return_value = IronClawResponse(
                type="response", response="Hello there!"
            )
            MockIC.return_value = mock_ic

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()
            result = await orch.handle_message("hi", user_id="U1", channel="C1")
            assert result == "Hello there!"
            mock_ic.interpret.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_message_with_tool_call(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            mock_ic = AsyncMock()
            mock_ic.interpret.side_effect = [
                IronClawResponse(
                    type="action_plan",
                    actions=[IronClawAction(tool="test.tool", args={"key": "val"})],
                ),
                IronClawResponse(type="response", response="Tool result processed."),
            ]
            MockIC.return_value = mock_ic

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()

            async def mock_tool(**kwargs):
                return f"executed with {kwargs}"

            orch.register_tool("test.tool", mock_tool, "A test tool")
            result = await orch.handle_message("do something")
            assert result == "Tool result processed."
            assert mock_ic.interpret.call_count == 2

    @pytest.mark.asyncio
    async def test_execute_tool_unknown(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            MockIC.return_value = AsyncMock()

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()
            with pytest.raises(KeyError, match="Unknown tool"):
                await orch.execute_tool("nonexistent.tool", {})

    @pytest.mark.asyncio
    async def test_execute_tool_persists_output(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            MockIC.return_value = AsyncMock()

            from agent.orchestrator import Orchestrator
            from database.models import ToolOutput

            orch = Orchestrator()

            async def mock_tool(**kwargs):
                return "tool_result"

            orch.register_tool("test.tool", mock_tool, "test")
            await orch.execute_tool("test.tool", {"arg": "val"})

            rows = db_session.query(ToolOutput).all()
            assert len(rows) == 1
            assert rows[0].tool_name == "test.tool"
            assert "tool_result" in rows[0].output_data

    @pytest.mark.asyncio
    async def test_execute_sync_tool(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            MockIC.return_value = AsyncMock()

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()

            def sync_tool(**kwargs):
                return "sync_result"

            orch.register_tool("sync.tool", sync_tool, "sync test")
            result = await orch.execute_tool("sync.tool", {})
            assert result == "sync_result"

    @pytest.mark.asyncio
    async def test_execute_tool_handles_exception(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            MockIC.return_value = AsyncMock()

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()

            async def failing_tool(**kwargs):
                raise ValueError("tool broke")

            orch.register_tool("bad.tool", failing_tool, "bad")
            result = await orch.execute_tool("bad.tool", {})
            assert "Error:" in result

    @pytest.mark.asyncio
    async def test_register_tool_with_schema(self, db_session):
        with patch("agent.orchestrator.IronClawClient") as MockIC:
            MockIC.return_value = AsyncMock()

            from agent.orchestrator import Orchestrator

            orch = Orchestrator()
            params = {"type": "object", "properties": {"x": {"type": "string"}}}
            orch.register_tool("test.t", lambda: None, "desc", params)
            schemas = orch.registry.get_all_schemas()
            assert len(schemas) == 1
            assert schemas[0]["parameters"] == params
