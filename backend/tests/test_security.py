"""Unit tests for security.secrets."""

import hashlib
import hmac
import logging

from security.secrets import (
    AppSecrets,
    RedactingFilter,
    get_secrets,
    redact,
    verify_webhook_signature,
)


class TestAppSecrets:
    def test_defaults(self):
        s = get_secrets()
        assert s.ironclaw_url == "http://localhost:9090"
        assert s.database_url == "sqlite://"
        assert s.webhook_port == 8080

    def test_slack_fields(self):
        s = get_secrets()
        assert s.slack_bot_token == ""
        assert s.slack_signing_secret == ""


class TestRedact:
    def test_redact_slack_token(self):
        text = "token is xoxb-1234-5678-abcdef"
        result = redact(text)
        assert "xoxb-" not in result
        assert "<REDACTED>" in result

    def test_redact_github_token(self):
        text = "ghp_abc123def456"
        result = redact(text)
        assert "ghp_" not in result

    def test_redact_bearer(self):
        text = "Authorization: Bearer eyJhbGci.test.token"
        result = redact(text)
        assert "eyJhbGci" not in result

    def test_no_redaction_needed(self):
        text = "this is a normal message"
        assert redact(text) == text


class TestVerifyWebhookSignature:
    def test_valid_signature(self):
        payload = b'{"action":"opened"}'
        secret = "mysecret"
        mac = hmac.new(secret.encode(), payload, hashlib.sha256)
        signature = f"sha256={mac.hexdigest()}"
        assert verify_webhook_signature(payload, signature, secret) is True

    def test_invalid_signature(self):
        payload = b'{"action":"opened"}'
        assert (
            verify_webhook_signature(payload, "sha256=badhex", "secret") is False
        )

    def test_empty_signature(self):
        assert verify_webhook_signature(b"data", "", "secret") is False


class TestRedactingFilter:
    def test_filter_redacts_msg(self):
        filt = RedactingFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="token is xoxb-1234-5678-abcdef",
            args=(),
            exc_info=None,
        )
        filt.filter(record)
        assert "xoxb-" not in record.msg
        assert "<REDACTED>" in record.msg

    def test_filter_redacts_args(self):
        filt = RedactingFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Token: %s",
            args=("ghp_abcdef123456",),
            exc_info=None,
        )
        filt.filter(record)
        assert "ghp_" not in record.args[0]
