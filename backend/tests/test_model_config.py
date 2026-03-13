"""Tests for model configuration, OpenRouter fallback, and agent logs.

Covers:
- IronClaw model switching (runtime)
- OpenRouter fallback on Ollama failure
- Model test endpoint
- API endpoints: GET/POST /api/model-config, /api/openrouter-key, /api/logs
- Agent log persistence and search
"""

import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from agent.ironclaw import IronClawClient, OLLAMA_MODELS, OPENROUTER_MODELS


def _mock_response(status_code: int, json_data: dict) -> httpx.Response:
    request = httpx.Request("POST", "http://test")
    return httpx.Response(status_code, json=json_data, request=request)


def _mock_get_response(status_code: int, json_data: dict) -> httpx.Response:
    request = httpx.Request("GET", "http://test")
    return httpx.Response(status_code, json=json_data, request=request)


# ─── IronClaw Model Switching ────────────────────────────────────────────────

class TestIronClawModelConfig:
    def test_default_model_from_env(self):
        client = IronClawClient()
        assert client.current_model == "qwen3.5:latest"
        assert client.current_provider == "ollama"

    def test_set_model_ollama(self):
        client = IronClawClient()
        result = client.set_model("llama3.2:latest", "ollama")
        assert result["model"] == "llama3.2:latest"
        assert result["provider"] == "ollama"
        assert client.current_model == "llama3.2:latest"

    def test_set_model_openrouter(self):
        client = IronClawClient()
        result = client.set_model("openai/gpt-4o-mini", "openrouter")
        assert result["provider"] == "openrouter"
        assert client.current_model == "openai/gpt-4o-mini"
        assert client.current_provider == "openrouter"

    def test_switch_back_to_ollama(self):
        client = IronClawClient()
        client.set_model("openai/gpt-4o-mini", "openrouter")
        client.set_model("phi3:3.8b", "ollama")
        assert client.current_model == "phi3:3.8b"
        assert client.current_provider == "ollama"

    def test_model_lists_populated(self):
        assert "qwen3.5:latest" in OLLAMA_MODELS
        assert "llama3.2:latest" in OLLAMA_MODELS
        assert "gemma3:4b" in OLLAMA_MODELS
        assert "phi3:3.8b" in OLLAMA_MODELS
        assert len(OPENROUTER_MODELS) >= 3

    @pytest.mark.asyncio
    async def test_interpret_uses_current_model(self):
        client = IronClawClient()
        client.set_model("phi3:3.8b", "ollama")
        mock_resp = _mock_response(200, {
            "id": "test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            await client.interpret("test", tools=[])
            payload = mock_instance.post.call_args.kwargs.get("json") or mock_instance.post.call_args[1].get("json")
            assert payload["model"] == "phi3:3.8b"

    @pytest.mark.asyncio
    async def test_summarize_uses_current_model(self):
        client = IronClawClient()
        client.set_model("gemma3:4b", "ollama")
        mock_resp = _mock_response(200, {
            "choices": [{"message": {"content": "summary"}}],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            await client.summarize("some content")
            payload = mock_instance.post.call_args.kwargs.get("json") or mock_instance.post.call_args[1].get("json")
            assert payload["model"] == "gemma3:4b"


# ─── OpenRouter Fallback ────────────────────────────────────────────────────

class TestOpenRouterFallback:
    @pytest.mark.asyncio
    async def test_fallback_on_ollama_failure(self):
        """When Ollama fails and OpenRouter key is set, should fallback."""
        client = IronClawClient()
        client._openrouter_api_key = "sk-or-test"
        client._provider = "ollama"

        ollama_fail = httpx.ConnectError("Connection refused")
        openrouter_ok = _mock_response(200, {
            "choices": [{"message": {"role": "assistant", "content": "fallback response"}}],
        })

        call_count = 0

        async def mock_post(url, json=None, headers=None):
            nonlocal call_count
            call_count += 1
            if "openrouter" in url:
                return openrouter_ok
            raise ollama_fail

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post = mock_post
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.summarize("content")
            assert result == "fallback response"
            assert call_count == 2

    @pytest.mark.asyncio
    async def test_no_fallback_without_key(self):
        """Without OpenRouter key, Ollama failure should raise."""
        client = IronClawClient()
        client._openrouter_api_key = ""

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.ConnectError("fail")
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            with pytest.raises(httpx.ConnectError):
                await client.summarize("content")

    @pytest.mark.asyncio
    async def test_openrouter_uses_correct_headers(self):
        client = IronClawClient()
        client._openrouter_api_key = "sk-or-test-key"
        client._provider = "openrouter"

        url, headers = client._completion_url()
        assert "openrouter" in url
        assert headers["Authorization"] == "Bearer sk-or-test-key"
        assert "X-Title" in headers

    @pytest.mark.asyncio
    async def test_ollama_provider_uses_ironclaw_url(self):
        client = IronClawClient()
        client._provider = "ollama"
        url, headers = client._completion_url()
        assert "localhost:9090" in url
        assert "X-Title" not in headers


# ─── Model Test ──────────────────────────────────────────────────────────────

class TestModelTest:
    @pytest.mark.asyncio
    async def test_model_test_success(self):
        client = IronClawClient()
        mock_resp = _mock_response(200, {
            "choices": [{"message": {"content": "Hello"}}],
        })
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.test_model("qwen3.5:latest", "ollama")
            assert result["ok"] is True
            assert result["response"] == "Hello"

    @pytest.mark.asyncio
    async def test_model_test_failure(self):
        client = IronClawClient()
        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.ConnectError("refused")
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.test_model("bad-model", "ollama")
            assert result["ok"] is False
            assert "refused" in result["error"]


# ─── API Endpoints ───────────────────────────────────────────────────────────

class TestModelConfigAPI:
    @pytest.fixture()
    def client(self):
        from webhooks.server import app
        return TestClient(app, raise_server_exceptions=False)

    def test_get_model_config(self, client):
        from webhooks.server import app
        from agent.ironclaw import IronClawClient
        orch = MagicMock()
        orch.ironclaw = IronClawClient()
        app.state.orchestrator = orch

        resp = client.get("/api/model-config")
        assert resp.status_code == 200
        data = resp.json()
        assert "ollama_models" in data
        assert "openrouter_models" in data
        assert data["current_provider"] == "ollama"
        assert data["current_model"] == "qwen3.5:latest"

    def test_get_model_config_no_orchestrator(self, client):
        from webhooks.server import app
        if hasattr(app.state, "orchestrator"):
            delattr(app.state, "orchestrator")
        resp = client.get("/api/model-config")
        assert resp.status_code == 200
        data = resp.json()
        assert data["current_model"] == "unknown"

    def test_set_model_missing_field(self, client):
        resp = client.post("/api/model-config", json={"provider": "ollama"})
        assert resp.status_code == 400

    def test_set_model_invalid_provider(self, client):
        resp = client.post("/api/model-config", json={"model": "test", "provider": "azure"})
        assert resp.status_code == 400

    def test_set_openrouter_without_key(self, client):
        from webhooks.server import app
        from agent.ironclaw import IronClawClient
        orch = MagicMock()
        orch.ironclaw = IronClawClient()
        app.state.orchestrator = orch

        resp = client.post("/api/model-config", json={"model": "openai/gpt-4o", "provider": "openrouter"})
        assert resp.status_code == 400
        assert "API key" in resp.json()["detail"]

    def test_set_openrouter_key(self, client):
        from webhooks.server import app
        from agent.ironclaw import IronClawClient
        orch = MagicMock()
        ic = IronClawClient()
        orch.ironclaw = ic
        app.state.orchestrator = orch

        resp = client.post("/api/openrouter-key", json={"api_key": "sk-or-test"})
        assert resp.status_code == 200
        assert ic._openrouter_api_key == "sk-or-test"

    def test_set_openrouter_key_empty(self, client):
        resp = client.post("/api/openrouter-key", json={"api_key": ""})
        assert resp.status_code == 400


# ─── Agent Logs API ──────────────────────────────────────────────────────────

class TestAgentLogsAPI:
    @pytest.fixture()
    def client(self):
        from webhooks.server import app
        return TestClient(app, raise_server_exceptions=False)

    def test_get_logs_empty(self, client):
        resp = client.get("/api/logs")
        assert resp.status_code == 200
        data = resp.json()
        assert data["logs"] == []
        assert data["total"] == 0

    def test_logs_persisted_and_retrieved(self, client, db_session):
        from database.models import AgentLog
        db_session.add(AgentLog(level="INFO", source="webhook.github", message="Received: github.push", detail="{}"))
        db_session.add(AgentLog(level="WARN", source="model-config", message="Model test failed", detail="timeout"))
        db_session.add(AgentLog(level="ERROR", source="webhook.slack", message="Slack signature invalid", detail=""))
        db_session.commit()

        resp = client.get("/api/logs")
        data = resp.json()
        assert data["total"] == 3
        assert len(data["logs"]) == 3

    def test_logs_search(self, client, db_session):
        from database.models import AgentLog
        db_session.add(AgentLog(level="INFO", source="webhook.github", message="PR opened"))
        db_session.add(AgentLog(level="INFO", source="webhook.jira", message="Ticket created"))
        db_session.commit()

        resp = client.get("/api/logs?search=PR")
        data = resp.json()
        assert data["total"] == 1
        assert "PR" in data["logs"][0]["message"]

    def test_logs_filter_level(self, client, db_session):
        from database.models import AgentLog
        db_session.add(AgentLog(level="INFO", source="test", message="info msg"))
        db_session.add(AgentLog(level="ERROR", source="test", message="error msg"))
        db_session.commit()

        resp = client.get("/api/logs?level=ERROR")
        data = resp.json()
        assert data["total"] == 1
        assert data["logs"][0]["level"] == "ERROR"

    def test_logs_filter_source(self, client, db_session):
        from database.models import AgentLog
        db_session.add(AgentLog(level="INFO", source="webhook.github", message="gh event"))
        db_session.add(AgentLog(level="INFO", source="model-config", message="model switch"))
        db_session.commit()

        resp = client.get("/api/logs?source=model-config")
        data = resp.json()
        assert data["total"] == 1
        assert data["logs"][0]["source"] == "model-config"

    def test_logs_pagination(self, client, db_session):
        from database.models import AgentLog
        for i in range(5):
            db_session.add(AgentLog(level="INFO", source="test", message=f"log {i}"))
        db_session.commit()

        resp = client.get("/api/logs?limit=2&offset=0")
        data = resp.json()
        assert data["total"] == 5
        assert len(data["logs"]) == 2

    def test_persist_log_via_webhook(self, client, db_session):
        """Webhook handler should persist a log entry."""
        payload = {"action": "opened", "pull_request": {}}
        client.post(
            "/webhooks/github",
            content=json.dumps(payload),
            headers={"X-GitHub-Event": "pull_request"},
        )
        from database.models import AgentLog
        logs = db_session.query(AgentLog).filter(AgentLog.source == "webhook.github").all()
        assert len(logs) >= 1


# ─── Deployment: New DB Table Exists ─────────────────────────────────────────

class TestAgentLogTable:
    def test_agent_logs_table_exists(self):
        from database.models import Base
        assert "agent_logs" in Base.metadata.tables
