"""Slack Command Gateway — primary developer interface.

Handles @claw mentions and slash commands from Slack, delegates
reasoning to IronClaw via the orchestrator, and posts responses
back to the originating Slack channel/thread.

Examples:
    @claw summarize today's PRs
    @claw investigate Jenkins build 1234
    @claw create Jira ticket from this email
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from events.types import AgentEvent

logger = logging.getLogger("claw-agent.slack-gateway")


class SlackCommandGateway:
    """Routes Slack messages mentioning @claw to the orchestrator
    and sends results back to Slack."""

    def __init__(self, orchestrator: Any, slack_integration: Any) -> None:
        self._orchestrator = orchestrator
        self._slack = slack_integration

    async def handle_event(self, event: AgentEvent) -> None:
        """Process a Slack event that may contain a @claw command."""
        slack_event = event.payload.get("event", {})
        event_type = slack_event.get("type", "")

        if event_type == "app_mention":
            await self._handle_mention(slack_event)
        elif event_type == "message":
            text = slack_event.get("text", "")
            if "@claw" in text.lower() or "claw" in text.lower():
                await self._handle_mention(slack_event)

    async def _handle_mention(self, slack_event: dict[str, Any]) -> None:
        """Extract command text, send to orchestrator, reply in Slack."""
        raw_text = slack_event.get("text", "")
        user_id = slack_event.get("user", "unknown")
        channel = slack_event.get("channel", "")
        thread_ts = slack_event.get("thread_ts") or slack_event.get("ts", "")

        command_text = self._extract_command(raw_text)
        if not command_text:
            return

        logger.info(
            "Slack command from user=%s channel=%s: %s",
            user_id,
            channel,
            command_text[:200],
        )

        try:
            response = await self._orchestrator.handle_message(
                user_message=command_text,
                user_id=user_id,
                channel=channel,
                conversation_id=thread_ts,
            )

            if self._slack:
                self._post_reply(channel, response, thread_ts)
        except Exception:
            logger.exception("Failed to handle Slack command")
            if self._slack:
                self._post_reply(
                    channel,
                    "Sorry, I encountered an error processing your request.",
                    thread_ts,
                )

    def _extract_command(self, text: str) -> str:
        """Strip the @claw mention prefix from the message text."""
        import re

        cleaned = re.sub(r"<@[A-Z0-9]+>", "", text).strip()
        return cleaned

    def _post_reply(self, channel: str, text: str, thread_ts: str) -> None:
        """Send a threaded reply back to Slack."""
        try:
            self._slack.send_message(
                channel=channel, text=text, thread_ts=thread_ts
            )
        except Exception:
            logger.exception("Failed to post Slack reply")
