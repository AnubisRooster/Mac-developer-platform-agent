"""Edge case and error handling tests across all modules.

Tests for boundary conditions, failure modes, and defensive behavior
that ensure reliable deployment.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from agent.ironclaw import IronClawClient, IronClawResponse
from agent.orchestrator import Orchestrator
from agent.slack_gateway import SlackCommandGateway
from events.types import AgentEvent, EventSource
from workflows.engine import WorkflowEngine
from workflows.loader import WorkflowAction, WorkflowDefinition


# ─── IronClaw Client Edge Cases ──────────────────────────────────────────────

def _mock_response(status_code: int, json_data: dict) -> httpx.Response:
    request = httpx.Request("POST", "http://test")
    return httpx.Response(status_code, json=json_data, request=request)


class TestIronClawEdgeCases:
    @pytest.mark.asyncio
    async def test_interpret_with_context(self):
        client = IronClawClient()
        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            context = [{"role": "user", "content": "previous"}, {"role": "assistant", "content": "response"}]
            result = await client.interpret("follow up", tools=[], context=context)
            payload = mock_instance.post.call_args.kwargs.get("json") or mock_instance.post.call_args[1].get("json")
            assert len(payload["messages"]) == 3  # 2 context + 1 new

    @pytest.mark.asyncio
    async def test_interpret_with_conversation_id(self):
        client = IronClawClient()
        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.interpret("test", tools=[], conversation_id="my-conv-123")
            assert result.conversation_id == "my-conv-123"

    @pytest.mark.asyncio
    async def test_interpret_malformed_tool_args(self):
        """When IronClaw returns invalid JSON in tool_calls arguments."""
        client = IronClawClient()
        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "tool_calls": [{
                        "id": "call_0",
                        "type": "function",
                        "function": {"name": "broken.tool", "arguments": "not-valid-json{{{"},
                    }],
                },
                "finish_reason": "tool_calls",
            }],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.interpret("test", tools=[])
            assert result.type == "action_plan"
            assert result.actions[0].tool == "broken.tool"
            assert result.actions[0].args == {}

    @pytest.mark.asyncio
    async def test_headers_without_token(self):
        client = IronClawClient()
        client._auth_token = ""
        headers = client._headers()
        assert "Authorization" not in headers

    @pytest.mark.asyncio
    async def test_headers_with_token(self):
        client = IronClawClient()
        client._auth_token = "my-secret"
        headers = client._headers()
        assert headers["Authorization"] == "Bearer my-secret"

    @pytest.mark.asyncio
    async def test_interpret_empty_choices(self):
        """When IronClaw returns an empty choices array."""
        client = IronClawClient()
        mock_resp = _mock_response(200, {"id": "chatcmpl-test", "choices": []})
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.interpret("test", tools=[])
            assert result.type == "response"
            assert result.response == ""


# ─── Orchestrator Edge Cases ─────────────────────────────────────────────────

class TestOrchestratorEdgeCases:
    @pytest.mark.asyncio
    async def test_handle_message_max_iterations(self):
        """Orchestrator should return fallback after 10 iterations of action_plans."""
        orch = Orchestrator()

        action_resp = IronClawResponse(
            type="action_plan",
            actions=[],
            conversation_id="conv",
        )
        orch._ironclaw.interpret = AsyncMock(return_value=action_resp)

        result = await orch.handle_message("loop forever")
        assert "iteration limit" in result.lower()

    @pytest.mark.asyncio
    async def test_execute_tool_unknown_raises(self):
        orch = Orchestrator()
        with pytest.raises(KeyError, match="Unknown tool"):
            await orch.execute_tool("nonexistent.tool", {})

    @pytest.mark.asyncio
    async def test_execute_tool_returns_none(self):
        orch = Orchestrator()
        orch.register_tool("returns.none", lambda: None, "Returns nothing")
        result = await orch.execute_tool("returns.none", {})
        assert result == ""

    @pytest.mark.asyncio
    async def test_execute_tool_exception_returns_error_string(self):
        def _explode(**kwargs):
            raise ValueError("kaboom")
        orch = Orchestrator()
        orch.register_tool("exploding.tool", _explode, "Blows up")
        result = await orch.execute_tool("exploding.tool", {})
        assert "kaboom" in result

    @pytest.mark.asyncio
    async def test_execute_tool_async_function(self):
        async def _async_tool(x: int = 0) -> str:
            return f"got {x}"
        orch = Orchestrator()
        orch.register_tool("async.tool", _async_tool, "Async tool")
        result = await orch.execute_tool("async.tool", {"x": 42})
        assert "42" in result

    @pytest.mark.asyncio
    async def test_persist_conversation_failure_does_not_raise(self):
        """_persist_conversation should log but not crash on DB errors."""
        orch = Orchestrator()
        with patch("agent.orchestrator.get_session", side_effect=Exception("DB down")):
            orch._persist_conversation(
                user_id="u1", channel="c1", conversation_id="conv1",
                user_message="hi", agent_response="hello", tools_used=[],
            )


# ─── Slack Gateway Edge Cases ────────────────────────────────────────────────

class TestSlackGatewayEdgeCases:
    @pytest.mark.asyncio
    async def test_message_with_claw_keyword(self):
        """Messages containing 'claw' (not app_mention) should be handled."""
        mock_orch = AsyncMock()
        mock_orch.handle_message.return_value = "response"
        mock_slack = MagicMock()
        gw = SlackCommandGateway(mock_orch, mock_slack)

        event = AgentEvent(
            event_type="slack.message.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "message",
                    "text": "hey claw can you help?",
                    "user": "U01",
                    "channel": "C01",
                    "ts": "123.456",
                }
            },
        )
        await gw.handle_event(event)
        mock_orch.handle_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_message_without_claw_ignored(self):
        mock_orch = AsyncMock()
        mock_slack = MagicMock()
        gw = SlackCommandGateway(mock_orch, mock_slack)

        event = AgentEvent(
            event_type="slack.message.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "message",
                    "text": "just a normal message",
                    "user": "U01",
                    "channel": "C01",
                }
            },
        )
        await gw.handle_event(event)
        mock_orch.handle_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_empty_command_after_extraction(self):
        """When the mention tag is stripped and nothing remains."""
        mock_orch = AsyncMock()
        mock_slack = MagicMock()
        gw = SlackCommandGateway(mock_orch, mock_slack)

        event = AgentEvent(
            event_type="slack.app_mention.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "app_mention",
                    "text": "<@U999BOT>",
                    "user": "U01",
                    "channel": "C01",
                    "ts": "123.456",
                }
            },
        )
        await gw.handle_event(event)
        mock_orch.handle_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_slack_is_none(self):
        """Gateway should not crash when slack_integration is None."""
        mock_orch = AsyncMock()
        mock_orch.handle_message.return_value = "response"
        gw = SlackCommandGateway(mock_orch, None)

        event = AgentEvent(
            event_type="slack.app_mention.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "app_mention",
                    "text": "<@U999BOT> do something",
                    "user": "U01",
                    "channel": "C01",
                    "ts": "123.456",
                }
            },
        )
        await gw.handle_event(event)
        mock_orch.handle_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_post_reply_exception_does_not_crash(self):
        mock_orch = AsyncMock()
        mock_orch.handle_message.return_value = "response"
        mock_slack = MagicMock()
        mock_slack.send_message.side_effect = Exception("Slack API down")
        gw = SlackCommandGateway(mock_orch, mock_slack)

        event = AgentEvent(
            event_type="slack.app_mention.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "app_mention",
                    "text": "<@U999BOT> test",
                    "user": "U01",
                    "channel": "C01",
                    "ts": "123.456",
                }
            },
        )
        await gw.handle_event(event)


# ─── Workflow Engine Edge Cases ──────────────────────────────────────────────

class TestWorkflowEngineEdgeCases:
    @pytest.mark.asyncio
    async def test_run_workflow_tool_not_found_stop(self):
        engine = WorkflowEngine()
        wf = WorkflowDefinition(
            name="test_wf",
            trigger="test.event",
            actions=[WorkflowAction(tool="missing.tool", on_failure="stop")],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        result = await engine.run_workflow(wf, event)
        assert result["status"] == "failed"

    @pytest.mark.asyncio
    async def test_run_workflow_tool_not_found_continue(self):
        def _good_tool(**kwargs):
            return "ok"
        engine = WorkflowEngine()
        engine.register_tool("good.tool", _good_tool)
        wf = WorkflowDefinition(
            name="test_wf",
            trigger="test.event",
            actions=[
                WorkflowAction(tool="missing.tool", on_failure="continue"),
                WorkflowAction(tool="good.tool"),
            ],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        result = await engine.run_workflow(wf, event)
        assert result["status"] == "completed"
        assert len(result["results"]) == 2

    @pytest.mark.asyncio
    async def test_run_workflow_tool_exception_stop(self):
        def _boom(**kwargs):
            raise RuntimeError("tool crashed")
        engine = WorkflowEngine()
        engine.register_tool("boom.tool", _boom)
        wf = WorkflowDefinition(
            name="test_wf",
            trigger="test.event",
            actions=[WorkflowAction(tool="boom.tool", on_failure="stop")],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        result = await engine.run_workflow(wf, event)
        assert result["status"] == "failed"

    @pytest.mark.asyncio
    async def test_run_workflow_persists_to_db(self, db_session):
        def _ok_tool(**kwargs):
            return "done"
        engine = WorkflowEngine()
        engine.register_tool("ok.tool", _ok_tool)
        wf = WorkflowDefinition(
            name="persist_wf",
            trigger="test.event",
            actions=[WorkflowAction(tool="ok.tool")],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        await engine.run_workflow(wf, event)

        from database.models import WorkflowRun
        runs = db_session.query(WorkflowRun).filter_by(workflow_name="persist_wf").all()
        assert len(runs) == 1
        assert runs[0].status == "completed"

    @pytest.mark.asyncio
    async def test_run_workflow_async_tool(self):
        async def _async_tool(**kwargs):
            return "async done"
        engine = WorkflowEngine()
        engine.register_tool("async.tool", _async_tool)
        wf = WorkflowDefinition(
            name="async_wf",
            trigger="test.event",
            actions=[WorkflowAction(tool="async.tool")],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        result = await engine.run_workflow(wf, event)
        assert result["status"] == "completed"

    def test_get_workflows_returns_dicts(self):
        engine = WorkflowEngine()
        engine._workflows = {
            "test.event": WorkflowDefinition(
                name="wf1", trigger="test.event", actions=[]
            )
        }
        wfs = engine.get_workflows()
        assert len(wfs) == 1
        assert wfs[0]["name"] == "wf1"

    @pytest.mark.asyncio
    async def test_handle_event_no_matching_workflow(self):
        engine = WorkflowEngine()
        event = AgentEvent(event_type="no.match", source=EventSource.SYSTEM)
        await engine._handle_event(event)

    @pytest.mark.asyncio
    async def test_run_workflow_step_payload_merge(self):
        """Previous step results should be merged into later step payloads."""
        call_log = []

        def _step1(**kwargs):
            return {"extra_key": "from_step1"}

        def _step2(**kwargs):
            call_log.append(kwargs)
            return "final"

        engine = WorkflowEngine()
        engine.register_tool("step1", _step1)
        engine.register_tool("step2", _step2)
        wf = WorkflowDefinition(
            name="merge_wf",
            trigger="test.event",
            actions=[
                WorkflowAction(tool="step1"),
                WorkflowAction(tool="step2"),
            ],
        )
        event = AgentEvent(event_type="test.event", source=EventSource.SYSTEM, payload={"initial": "data"})
        await engine.run_workflow(wf, event)
        assert "extra_key" in call_log[0]
        assert call_log[0]["extra_key"] == "from_step1"


# ─── Security Edge Cases ────────────────────────────────────────────────────

class TestSecurityEdgeCases:
    def test_redact_xapp_token(self):
        from security.secrets import redact
        assert "<REDACTED>" in redact("token is xapp-1234-abcdef")

    def test_redact_gho_token(self):
        from security.secrets import redact
        assert "<REDACTED>" in redact("token is gho_abc123xyz")

    def test_redact_sk_token(self):
        from security.secrets import redact
        assert "<REDACTED>" in redact("key is sk-abc123def456")

    def test_redact_bearer_token(self):
        from security.secrets import redact
        assert "<REDACTED>" in redact('Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.test')

    def test_redact_token_equals_pattern(self):
        from security.secrets import redact
        assert "<REDACTED>" in redact("token='my-secret-value'")

    def test_verify_webhook_sha1(self):
        """verify_webhook_signature should work with sha1 too."""
        import hashlib, hmac as _hmac
        from security.secrets import verify_webhook_signature
        payload = b"test-payload"
        secret = "my-secret"
        mac = _hmac.new(secret.encode(), payload, hashlib.sha1)
        sig = f"sha1={mac.hexdigest()}"
        assert verify_webhook_signature(payload, sig, secret, "sha1")


# ─── API Endpoints Edge Cases ────────────────────────────────────────────────

class TestAPIEndpointEdgeCases:
    @pytest.fixture()
    def client(self):
        from fastapi.testclient import TestClient
        from webhooks.server import app
        return TestClient(app, raise_server_exceptions=False)

    def test_api_status_no_orchestrator(self, client):
        """Status should work even when orchestrator isn't attached."""
        from webhooks.server import app
        if hasattr(app.state, "orchestrator"):
            delattr(app.state, "orchestrator")
        resp = client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ironclaw"]["status"] == "not_configured"

    def test_api_tools_no_orchestrator(self, client):
        from webhooks.server import app
        if hasattr(app.state, "orchestrator"):
            delattr(app.state, "orchestrator")
        resp = client.get("/api/tools")
        assert resp.status_code == 200
        assert resp.json()["tools"] == []

    def test_api_workflows_no_engine(self, client):
        from webhooks.server import app
        if hasattr(app.state, "workflow_engine"):
            delattr(app.state, "workflow_engine")
        resp = client.get("/api/workflows")
        assert resp.status_code == 200
        assert resp.json()["workflows"] == []

    def test_api_events_pagination(self, client, db_session):
        from database.models import Event
        for i in range(5):
            db_session.add(Event(event_type=f"test.event.{i}", source="system", payload="{}"))
        db_session.commit()

        resp = client.get("/api/events?limit=2&offset=0")
        data = resp.json()
        assert data["total"] == 5
        assert len(data["events"]) == 2

        resp2 = client.get("/api/events?limit=2&offset=2")
        data2 = resp2.json()
        assert len(data2["events"]) == 2

    def test_api_conversations_pagination(self, client, db_session):
        from database.models import AgentConversation
        for i in range(3):
            db_session.add(AgentConversation(
                conversation_id=f"conv-{i}", user_id="u1", channel="c1",
                user_message=f"msg {i}", agent_response=f"resp {i}",
            ))
        db_session.commit()

        resp = client.get("/api/agent-conversations?limit=2")
        data = resp.json()
        assert data["total"] == 3
        assert len(data["conversations"]) == 2
