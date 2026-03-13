"""Unit tests for events.types and events.bus."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from events.types import AgentEvent, EventSource


class TestEventSource:
    def test_values(self):
        assert EventSource.GITHUB.value == "github"
        assert EventSource.SLACK.value == "slack"
        assert EventSource.JENKINS.value == "jenkins"
        assert EventSource.JIRA.value == "jira"
        assert EventSource.SYSTEM.value == "system"


class TestAgentEvent:
    def test_defaults(self):
        ev = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        assert ev.event_type == "test.event"
        assert ev.source == EventSource.SYSTEM
        assert ev.payload == {}
        assert ev.id  # auto-generated
        assert ev.timestamp

    def test_with_payload(self):
        ev = AgentEvent(
            event_type="github.pr.opened",
            source=EventSource.GITHUB,
            payload={"action": "opened", "number": 42},
        )
        assert ev.payload["number"] == 42

    def test_str(self):
        ev = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        s = str(ev)
        assert "system" in s
        assert "test.event" in s


class TestEventBus:
    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self, db_session):
        from events.bus import EventBus

        bus = EventBus()
        handler = AsyncMock()
        bus.subscribe("test.event", handler)

        ev = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        await bus.publish(ev)

        handler.assert_called_once()
        received = handler.call_args[0][0]
        assert received.event_type == "test.event"

    @pytest.mark.asyncio
    async def test_wildcard_subscription(self, db_session):
        from events.bus import EventBus

        bus = EventBus()
        handler = AsyncMock()
        bus.subscribe("github.*", handler)

        ev = AgentEvent(
            event_type="github.pull_request.opened",
            source=EventSource.GITHUB,
        )
        await bus.publish(ev)
        handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_match(self, db_session):
        from events.bus import EventBus

        bus = EventBus()
        handler = AsyncMock()
        bus.subscribe("jira.issue.created", handler)

        ev = AgentEvent(
            event_type="github.pull_request.opened",
            source=EventSource.GITHUB,
        )
        await bus.publish(ev)
        handler.assert_not_called()

    @pytest.mark.asyncio
    async def test_global_subscriber(self, db_session):
        from events.bus import EventBus

        bus = EventBus()
        handler = AsyncMock()
        bus.subscribe_all(handler)

        ev = AgentEvent(event_type="any.event", source=EventSource.SYSTEM)
        await bus.publish(ev)
        handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_persists_event(self, db_session):
        from events.bus import EventBus
        from database.models import Event as EventRow

        bus = EventBus()
        ev = AgentEvent(
            event_type="test.persist",
            source=EventSource.SYSTEM,
            payload={"key": "value"},
        )
        await bus.publish(ev)

        rows = db_session.query(EventRow).all()
        assert len(rows) == 1
        assert rows[0].event_type == "test.persist"
        assert rows[0].source == "system"

    @pytest.mark.asyncio
    async def test_handler_exception_does_not_crash(self, db_session):
        from events.bus import EventBus

        bus = EventBus()
        bad_handler = AsyncMock(side_effect=RuntimeError("boom"))
        good_handler = AsyncMock()
        bus.subscribe("test.event", bad_handler)
        bus.subscribe("test.event", good_handler)

        ev = AgentEvent(event_type="test.event", source=EventSource.SYSTEM)
        await bus.publish(ev)

        bad_handler.assert_called_once()
        good_handler.assert_called_once()
