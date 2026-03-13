"""Integration tests for webhooks/server.py — webhook and dashboard API endpoints."""

import hashlib
import hmac
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from webhooks.server import app

    app.state.orchestrator = MagicMock()
    app.state.orchestrator.registry = MagicMock()
    app.state.orchestrator.registry.get_all_schemas.return_value = [
        {"name": "test.tool", "description": "A test", "parameters": {}}
    ]
    app.state.orchestrator.ironclaw = AsyncMock()
    app.state.orchestrator.ironclaw.health.return_value = {"status": "healthy"}
    app.state.workflow_engine = MagicMock()
    app.state.workflow_engine.get_workflows.return_value = [
        {"name": "test_wf", "trigger": "test.event", "description": "", "actions": [], "enabled": True}
    ]

    return TestClient(app)


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestGitHubWebhook:
    def test_github_webhook(self, client):
        payload = {"action": "opened", "pull_request": {"number": 42}}
        resp = client.post(
            "/webhooks/github",
            json=payload,
            headers={"X-GitHub-Event": "pull_request"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["accepted"] is True
        assert "github.pull_request.opened" == data["event_type"]


class TestJiraWebhook:
    def test_jira_webhook(self, client):
        payload = {"webhookEvent": "jira:issue_created", "issue": {"key": "TEST-1"}}
        resp = client.post("/webhooks/jira", json=payload)
        assert resp.status_code == 200
        assert resp.json()["accepted"] is True


class TestJenkinsWebhook:
    def test_jenkins_webhook(self, client):
        payload = {
            "name": "my-job",
            "build": {"phase": "COMPLETED", "status": "failure"},
        }
        resp = client.post("/webhooks/jenkins", json=payload)
        assert resp.status_code == 200
        assert resp.json()["accepted"] is True


class TestSlackWebhook:
    def test_slack_url_verification(self, client):
        payload = {"type": "url_verification", "challenge": "abc123"}
        resp = client.post("/webhooks/slack", json=payload)
        assert resp.status_code == 200
        assert resp.json()["challenge"] == "abc123"

    def test_slack_event(self, client):
        payload = {
            "type": "event_callback",
            "event": {"type": "app_mention", "text": "<@U123> hello"},
        }
        resp = client.post("/webhooks/slack", json=payload)
        assert resp.status_code == 200
        assert resp.json()["accepted"] is True


class TestDashboardAPIStatus:
    def test_api_status(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert "ironclaw" in data
        assert "database" in data
        assert "integrations" in data


class TestDashboardAPIEvents:
    def test_api_events_empty(self, client):
        resp = client.get("/api/events")
        assert resp.status_code == 200
        data = resp.json()
        assert data["events"] == []
        assert data["total"] == 0

    def test_api_events_with_data(self, client, db_session):
        from database.models import Event

        db_session.add(Event(event_type="test.event", source="system", payload="{}"))
        db_session.commit()

        resp = client.get("/api/events")
        data = resp.json()
        assert data["total"] == 1
        assert data["events"][0]["event_type"] == "test.event"


class TestDashboardAPIWorkflows:
    def test_api_workflows(self, client):
        resp = client.get("/api/workflows")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["workflows"]) == 1
        assert data["workflows"][0]["name"] == "test_wf"


class TestDashboardAPIWorkflowRuns:
    def test_api_workflow_runs_empty(self, client):
        resp = client.get("/api/workflow-runs")
        assert resp.status_code == 200
        assert resp.json()["runs"] == []

    def test_api_workflow_runs_with_data(self, client, db_session):
        from database.models import WorkflowRun

        db_session.add(
            WorkflowRun(
                workflow_name="test_wf",
                trigger_event="test.event",
                status="completed",
                result='[{"step":1}]',
            )
        )
        db_session.commit()

        resp = client.get("/api/workflow-runs")
        data = resp.json()
        assert data["total"] == 1
        assert data["runs"][0]["status"] == "completed"


class TestDashboardAPITools:
    def test_api_tools(self, client):
        resp = client.get("/api/tools")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tools"]) == 1
        assert data["tools"][0]["name"] == "test.tool"


class TestDashboardAPIConversations:
    def test_api_conversations_empty(self, client):
        resp = client.get("/api/agent-conversations")
        assert resp.status_code == 200
        assert resp.json()["conversations"] == []

    def test_api_conversations_with_data(self, client, db_session):
        from database.models import AgentConversation

        db_session.add(
            AgentConversation(
                conversation_id="t1",
                user_id="U1",
                channel="C1",
                user_message="hello",
                agent_response="hi",
                tools_used='["test.tool"]',
            )
        )
        db_session.commit()

        resp = client.get("/api/agent-conversations")
        data = resp.json()
        assert data["total"] == 1
        assert data["conversations"][0]["user_id"] == "U1"
        assert data["conversations"][0]["tools_used"] == ["test.tool"]
