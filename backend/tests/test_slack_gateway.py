"""Unit tests for agent.slack_gateway.SlackCommandGateway."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from agent.slack_gateway import SlackCommandGateway
from events.types import AgentEvent, EventSource


class TestSlackCommandGateway:
    def _make_gateway(self):
        mock_orch = AsyncMock()
        mock_orch.handle_message = AsyncMock(return_value="Agent response")
        mock_slack = MagicMock()
        mock_slack.send_message = MagicMock()
        return SlackCommandGateway(mock_orch, mock_slack), mock_orch, mock_slack

    @pytest.mark.asyncio
    async def test_handle_app_mention(self):
        gw, mock_orch, mock_slack = self._make_gateway()

        event = AgentEvent(
            event_type="slack.app_mention.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "app_mention",
                    "text": "<@U123> summarize today's PRs",
                    "user": "U456",
                    "channel": "C789",
                    "ts": "1234567890.123456",
                }
            },
        )

        await gw.handle_event(event)

        mock_orch.handle_message.assert_called_once()
        call_kwargs = mock_orch.handle_message.call_args
        assert "summarize today's PRs" in call_kwargs.kwargs["user_message"]
        assert call_kwargs.kwargs["user_id"] == "U456"
        assert call_kwargs.kwargs["channel"] == "C789"

        mock_slack.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_non_mention_ignored(self):
        gw, mock_orch, mock_slack = self._make_gateway()

        event = AgentEvent(
            event_type="slack.message.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "message",
                    "text": "just a normal message",
                    "user": "U456",
                    "channel": "C789",
                }
            },
        )

        await gw.handle_event(event)
        mock_orch.handle_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_error_sends_error_reply(self):
        gw, mock_orch, mock_slack = self._make_gateway()
        mock_orch.handle_message.side_effect = RuntimeError("IronClaw down")

        event = AgentEvent(
            event_type="slack.app_mention.received",
            source=EventSource.SLACK,
            payload={
                "event": {
                    "type": "app_mention",
                    "text": "<@U123> do something",
                    "user": "U456",
                    "channel": "C789",
                    "ts": "1234567890.123456",
                }
            },
        )

        await gw.handle_event(event)
        mock_slack.send_message.assert_called_once()
        error_text = mock_slack.send_message.call_args.kwargs["text"]
        assert "error" in error_text.lower()

    def test_extract_command(self):
        gw, _, _ = self._make_gateway()
        assert gw._extract_command("<@U123> summarize PRs") == "summarize PRs"
        assert gw._extract_command("plain text") == "plain text"
        assert gw._extract_command("<@U123>") == ""
