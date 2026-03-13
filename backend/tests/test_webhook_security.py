"""Webhook signature verification tests — ensure invalid requests are rejected.

These tests verify that:
- Missing GitHub signatures return 401
- Invalid GitHub signatures return 403
- Invalid Slack signatures return 403
- Jira/Jenkins webhooks enforce signature validation when secrets are set
"""

import hashlib
import hmac
import json
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def secured_client():
    """TestClient with webhook secrets configured."""
    os.environ["GITHUB_WEBHOOK_SECRET"] = "gh-secret-123"
    os.environ["JIRA_WEBHOOK_SECRET"] = "jira-secret-456"
    os.environ["JENKINS_WEBHOOK_SECRET"] = "jenkins-secret-789"
    os.environ["SLACK_SIGNING_SECRET"] = "slack-secret-abc"
    from security.secrets import get_secrets
    get_secrets.cache_clear()

    from webhooks.server import app
    client = TestClient(app, raise_server_exceptions=False)
    yield client

    os.environ["GITHUB_WEBHOOK_SECRET"] = ""
    os.environ["JIRA_WEBHOOK_SECRET"] = ""
    os.environ["JENKINS_WEBHOOK_SECRET"] = ""
    os.environ["SLACK_SIGNING_SECRET"] = ""
    get_secrets.cache_clear()


def _github_signature(body: bytes, secret: str) -> str:
    mac = hmac.new(secret.encode(), body, hashlib.sha256)
    return f"sha256={mac.hexdigest()}"


def _slack_signature(body: bytes, secret: str, timestamp: str) -> str:
    sig_basestring = f"v0:{timestamp}:{body.decode()}"
    mac = hmac.new(secret.encode(), sig_basestring.encode(), hashlib.sha256)
    return f"v0={mac.hexdigest()}"


class TestGitHubWebhookSecurity:
    def test_missing_signature_returns_401(self, secured_client):
        payload = {"action": "opened", "pull_request": {}}
        resp = secured_client.post(
            "/webhooks/github",
            content=json.dumps(payload),
            headers={"X-GitHub-Event": "pull_request"},
        )
        assert resp.status_code == 401

    def test_invalid_signature_returns_403(self, secured_client):
        payload = json.dumps({"action": "opened"}).encode()
        resp = secured_client.post(
            "/webhooks/github",
            content=payload,
            headers={
                "X-GitHub-Event": "pull_request",
                "X-Hub-Signature-256": "sha256=invalid",
            },
        )
        assert resp.status_code == 403

    def test_valid_signature_accepted(self, secured_client):
        payload = json.dumps({"action": "opened"}).encode()
        sig = _github_signature(payload, "gh-secret-123")
        resp = secured_client.post(
            "/webhooks/github",
            content=payload,
            headers={
                "X-GitHub-Event": "pull_request",
                "X-Hub-Signature-256": sig,
            },
        )
        assert resp.status_code == 200


class TestSlackWebhookSecurity:
    def test_invalid_slack_signature_returns_403(self, secured_client):
        payload = json.dumps({"type": "event_callback", "event": {"type": "message"}}).encode()
        resp = secured_client.post(
            "/webhooks/slack",
            content=payload,
            headers={
                "X-Slack-Request-Timestamp": "1234567890",
                "X-Slack-Signature": "v0=invalid_signature",
            },
        )
        assert resp.status_code == 403

    def test_valid_slack_signature_accepted(self, secured_client):
        payload = json.dumps({"type": "event_callback", "event": {"type": "message"}}).encode()
        timestamp = "1234567890"
        sig = _slack_signature(payload, "slack-secret-abc", timestamp)
        resp = secured_client.post(
            "/webhooks/slack",
            content=payload,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": sig,
            },
        )
        assert resp.status_code == 200

    def test_url_verification_challenge(self, secured_client):
        """Slack URL verification should work even with signing enabled."""
        payload_dict = {"type": "url_verification", "challenge": "test-challenge-xyz"}
        payload = json.dumps(payload_dict).encode()
        timestamp = "1234567890"
        sig = _slack_signature(payload, "slack-secret-abc", timestamp)
        resp = secured_client.post(
            "/webhooks/slack",
            content=payload,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": sig,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["challenge"] == "test-challenge-xyz"


class TestJiraWebhookSecurity:
    def test_invalid_jira_signature_returns_403(self, secured_client):
        payload = json.dumps({"webhookEvent": "jira:issue_created"}).encode()
        resp = secured_client.post(
            "/webhooks/jira",
            content=payload,
            headers={"X-Hub-Signature": "sha256=wrong"},
        )
        assert resp.status_code == 403


class TestJenkinsWebhookSecurity:
    def test_invalid_jenkins_signature_returns_403(self, secured_client):
        payload = json.dumps({"build": {"phase": "COMPLETED", "status": "FAILURE"}, "name": "job1"}).encode()
        resp = secured_client.post(
            "/webhooks/jenkins",
            content=payload,
            headers={"X-Jenkins-Signature": "sha256=wrong"},
        )
        assert resp.status_code == 403

    def test_no_signature_header_passes_when_secret_set(self, secured_client):
        """Jenkins webhook without signature header still passes (only rejects bad sigs)."""
        payload = json.dumps({"build": {"phase": "COMPLETED", "status": "SUCCESS"}, "name": "job1"}).encode()
        resp = secured_client.post(
            "/webhooks/jenkins",
            content=payload,
        )
        assert resp.status_code == 200
