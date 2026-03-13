"""Shared test fixtures — sets env vars, resets caches, provides mock helpers."""

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

BACKEND_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_ROOT.parent

# Ensure backend/ is first on sys.path and the old root-level packages don't shadow
project_root_str = str(PROJECT_ROOT)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
if str(BACKEND_ROOT) in sys.path:
    sys.path.remove(str(BACKEND_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))

os.environ.update(
    {
        "DATABASE_URL": "sqlite://",
        "IRONCLAW_URL": "http://localhost:9090",
        "SLACK_BOT_TOKEN": "",
        "SLACK_APP_TOKEN": "",
        "SLACK_SIGNING_SECRET": "",
        "GITHUB_TOKEN": "",
        "GITHUB_WEBHOOK_SECRET": "",
        "JIRA_URL": "",
        "JIRA_USER": "",
        "JIRA_API_TOKEN": "",
        "JIRA_WEBHOOK_SECRET": "",
        "CONFLUENCE_URL": "",
        "CONFLUENCE_USER": "",
        "CONFLUENCE_API_TOKEN": "",
        "JENKINS_URL": "",
        "JENKINS_USER": "",
        "JENKINS_API_TOKEN": "",
        "JENKINS_WEBHOOK_SECRET": "",
        "GMAIL_CREDENTIALS_FILE": "credentials.json",
        "GMAIL_TOKEN_FILE": "token.json",
        "WEBHOOK_HOST": "0.0.0.0",
        "WEBHOOK_PORT": "8080",
    }
)


@pytest.fixture(autouse=True)
def _reset_secrets_cache():
    """Clear the secrets singleton cache before and after each test."""
    from security.secrets import get_secrets

    get_secrets.cache_clear()
    yield
    get_secrets.cache_clear()


@pytest.fixture(autouse=True)
def _reset_db_globals():
    """Reset database engine/session globals so each test gets a fresh DB.

    Uses StaticPool so the same in-memory SQLite connection is shared
    across all get_session() calls within a test.
    """
    import database.models as dm
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    dm.Base.metadata.create_all(engine)
    dm._engine = engine
    dm._SessionLocal = sessionmaker(bind=engine)
    yield
    dm.Base.metadata.drop_all(engine)
    engine.dispose()
    dm._engine = None
    dm._SessionLocal = None


@pytest.fixture()
def db_session():
    """Provide a test database session backed by the shared in-memory SQLite."""
    from database.models import get_session

    session = get_session()
    yield session
    session.close()


@pytest.fixture()
def mock_ironclaw_response():
    """Factory for IronClaw OpenAI-compatible response dicts."""

    def _make(
        response_type="response",
        response_text="Here is the result.",
        actions=None,
    ):
        import json as _json

        if response_type == "action_plan" and actions:
            tool_calls = [
                {
                    "id": f"call_{i}",
                    "type": "function",
                    "function": {
                        "name": a["tool"],
                        "arguments": _json.dumps(a.get("args", {})),
                    },
                }
                for i, a in enumerate(actions)
            ]
            return {
                "id": "chatcmpl-test",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "tool_calls": tool_calls,
                        },
                        "finish_reason": "tool_calls",
                    }
                ],
            }
        return {
            "id": "chatcmpl-test",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text,
                    },
                    "finish_reason": "stop",
                }
            ],
        }

    return _make


@pytest.fixture()
def sample_tool_func():
    """A simple sync tool function for registry tests."""

    def _tool(channel: str = "", text: str = "") -> dict:
        return {"ok": True, "channel": channel, "text": text}

    return _tool


@pytest.fixture()
def async_tool_func():
    """A simple async tool function for orchestrator tests."""

    async def _tool(**kwargs) -> str:
        return f"result: {kwargs}"

    return _tool
