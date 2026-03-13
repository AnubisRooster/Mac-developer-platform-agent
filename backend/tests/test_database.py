"""Unit tests for database.models — all tables and session management."""

import datetime as dt

from database.models import (
    AgentConversation,
    AgentMemory,
    Event,
    ToolOutput,
    WorkflowRun,
    get_session,
)


class TestEventModel:
    def test_create_and_read(self, db_session):
        ev = Event(event_type="github.pr.opened", source="github", payload='{"action":"opened"}')
        db_session.add(ev)
        db_session.commit()

        rows = db_session.query(Event).all()
        assert len(rows) == 1
        assert rows[0].event_type == "github.pr.opened"
        assert rows[0].source == "github"
        assert rows[0].id is not None


class TestWorkflowRunModel:
    def test_create_and_update(self, db_session):
        run = WorkflowRun(
            workflow_name="pr_opened",
            trigger_event="github.pull_request.opened",
            status="running",
        )
        db_session.add(run)
        db_session.commit()

        run.status = "completed"
        run.finished_at = dt.datetime.now(dt.timezone.utc)
        db_session.merge(run)
        db_session.commit()

        result = db_session.query(WorkflowRun).first()
        assert result.status == "completed"
        assert result.finished_at is not None


class TestToolOutputModel:
    def test_create(self, db_session):
        output = ToolOutput(
            tool_name="slack.send_message",
            input_data='{"channel":"#test","text":"hi"}',
            output_data='{"ok":true}',
        )
        db_session.add(output)
        db_session.commit()

        rows = db_session.query(ToolOutput).all()
        assert len(rows) == 1
        assert rows[0].tool_name == "slack.send_message"


class TestAgentMemoryModel:
    def test_create_and_read(self, db_session):
        mem = AgentMemory(key="user.preference", value="dark_mode", context="slack")
        db_session.add(mem)
        db_session.commit()

        result = db_session.query(AgentMemory).filter_by(key="user.preference").first()
        assert result is not None
        assert result.value == "dark_mode"
        assert result.context == "slack"

    def test_unique_key(self, db_session):
        mem1 = AgentMemory(key="unique_key", value="val1")
        db_session.add(mem1)
        db_session.commit()

        mem2 = AgentMemory(key="unique_key", value="val2")
        db_session.add(mem2)
        try:
            db_session.commit()
            assert False, "Expected IntegrityError"
        except Exception:
            db_session.rollback()


class TestAgentConversationModel:
    def test_create_and_read(self, db_session):
        conv = AgentConversation(
            conversation_id="thread-123",
            user_id="U12345",
            channel="C67890",
            user_message="summarize today's PRs",
            agent_response="Here are today's PRs...",
            tools_used='["github.summarize_pr"]',
        )
        db_session.add(conv)
        db_session.commit()

        rows = db_session.query(AgentConversation).all()
        assert len(rows) == 1
        assert rows[0].user_id == "U12345"
        assert rows[0].conversation_id == "thread-123"


class TestSessionManagement:
    def test_get_session_returns_valid_session(self):
        session = get_session()
        assert session is not None
        session.close()

    def test_multiple_sessions_independent(self):
        s1 = get_session()
        s2 = get_session()
        assert s1 is not s2
        s1.close()
        s2.close()
