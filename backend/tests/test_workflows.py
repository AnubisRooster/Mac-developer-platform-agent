"""Unit tests for workflows.loader and workflows.engine."""

import tempfile
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml

from events.types import AgentEvent, EventSource
from workflows.loader import WorkflowAction, WorkflowDefinition, load_all_workflows, load_workflow


class TestWorkflowLoader:
    def test_load_workflow_from_yaml(self, tmp_path):
        wf_data = {
            "name": "test_workflow",
            "trigger": "github.pull_request.opened",
            "description": "A test workflow",
            "actions": [
                {"tool": "github.summarize_pr", "args": {"repo": "org/repo"}, "description": "Summarize PR"},
                {"tool": "slack.send_message", "args": {"channel": "#test"}, "description": "Notify"},
            ],
        }
        wf_file = tmp_path / "test.yaml"
        wf_file.write_text(yaml.dump(wf_data))

        wf = load_workflow(wf_file)
        assert wf.name == "test_workflow"
        assert wf.trigger == "github.pull_request.opened"
        assert len(wf.actions) == 2
        assert wf.actions[0].tool == "github.summarize_pr"
        assert wf.enabled is True

    def test_load_disabled_workflow(self, tmp_path):
        wf_data = {
            "name": "disabled_wf",
            "trigger": "test.event",
            "enabled": False,
            "actions": [{"tool": "test.tool"}],
        }
        wf_file = tmp_path / "disabled.yaml"
        wf_file.write_text(yaml.dump(wf_data))

        wf = load_workflow(wf_file)
        assert wf.enabled is False

    def test_load_all_workflows(self, tmp_path):
        for i in range(3):
            wf_data = {
                "name": f"wf_{i}",
                "trigger": f"event.type.{i}",
                "actions": [{"tool": f"tool.{i}"}],
            }
            (tmp_path / f"wf_{i}.yaml").write_text(yaml.dump(wf_data))

        workflows = load_all_workflows(str(tmp_path))
        assert len(workflows) == 3

    def test_load_all_skips_disabled(self, tmp_path):
        enabled = {"name": "enabled", "trigger": "a.b", "actions": [{"tool": "x"}]}
        disabled = {"name": "disabled", "trigger": "c.d", "enabled": False, "actions": [{"tool": "y"}]}
        (tmp_path / "enabled.yaml").write_text(yaml.dump(enabled))
        (tmp_path / "disabled.yaml").write_text(yaml.dump(disabled))

        workflows = load_all_workflows(str(tmp_path))
        assert len(workflows) == 1

    def test_load_all_nonexistent_dir(self):
        workflows = load_all_workflows("/nonexistent/path")
        assert workflows == {}


class TestWorkflowAction:
    def test_defaults(self):
        action = WorkflowAction(tool="test.tool")
        assert action.args == {}
        assert action.on_failure == "stop"
        assert action.description == ""


class TestWorkflowEngine:
    @pytest.mark.asyncio
    async def test_run_workflow(self, db_session):
        from events.bus import EventBus
        from workflows.engine import WorkflowEngine

        bus = EventBus()
        engine = WorkflowEngine(bus=bus, workflow_dir="/nonexistent")

        mock_tool = AsyncMock(return_value={"ok": True})
        engine.register_tool("test.tool", mock_tool)

        wf = WorkflowDefinition(
            name="test_wf",
            trigger="test.trigger",
            actions=[WorkflowAction(tool="test.tool", args={"arg": "val"})],
        )
        event = AgentEvent(event_type="test.trigger", source=EventSource.SYSTEM, payload={})

        result = await engine.run_workflow(wf, event)
        assert result["status"] == "completed"
        assert result["workflow"] == "test_wf"
        mock_tool.assert_called_once()

    @pytest.mark.asyncio
    async def test_workflow_tool_not_found(self, db_session):
        from events.bus import EventBus
        from workflows.engine import WorkflowEngine

        bus = EventBus()
        engine = WorkflowEngine(bus=bus, workflow_dir="/nonexistent")

        wf = WorkflowDefinition(
            name="missing_tool_wf",
            trigger="test.trigger",
            actions=[WorkflowAction(tool="nonexistent.tool")],
        )
        event = AgentEvent(event_type="test.trigger", source=EventSource.SYSTEM, payload={})

        result = await engine.run_workflow(wf, event)
        assert result["status"] == "failed"

    @pytest.mark.asyncio
    async def test_workflow_continue_on_failure(self, db_session):
        from events.bus import EventBus
        from workflows.engine import WorkflowEngine

        bus = EventBus()
        engine = WorkflowEngine(bus=bus, workflow_dir="/nonexistent")

        failing_tool = AsyncMock(side_effect=RuntimeError("boom"))
        ok_tool = AsyncMock(return_value="success")
        engine.register_tool("failing", failing_tool)
        engine.register_tool("ok", ok_tool)

        wf = WorkflowDefinition(
            name="continue_wf",
            trigger="test.trigger",
            actions=[
                WorkflowAction(tool="failing", on_failure="continue"),
                WorkflowAction(tool="ok"),
            ],
        )
        event = AgentEvent(event_type="test.trigger", source=EventSource.SYSTEM, payload={})

        result = await engine.run_workflow(wf, event)
        assert result["status"] == "completed"
        ok_tool.assert_called_once()

    @pytest.mark.asyncio
    async def test_event_triggers_workflow(self, db_session):
        from events.bus import EventBus
        from workflows.engine import WorkflowEngine

        bus = EventBus()
        engine = WorkflowEngine(bus=bus, workflow_dir="/nonexistent")

        mock_tool = AsyncMock(return_value="done")
        engine.register_tool("my.tool", mock_tool)

        engine._workflows = {
            "my.event": WorkflowDefinition(
                name="auto_wf",
                trigger="my.event",
                actions=[WorkflowAction(tool="my.tool")],
            )
        }
        bus.subscribe("my.event", engine._handle_event)

        event = AgentEvent(event_type="my.event", source=EventSource.SYSTEM, payload={})
        await bus.publish(event)

        mock_tool.assert_called_once()
