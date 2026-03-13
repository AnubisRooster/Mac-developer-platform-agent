"""Unit tests for agent.ironclaw.IronClawClient."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from agent.ironclaw import IronClawAction, IronClawClient, IronClawResponse


class TestIronClawResponse:
    def test_response_type(self):
        resp = IronClawResponse(type="response", response="Hello!")
        assert resp.type == "response"
        assert resp.response == "Hello!"
        assert resp.actions == []

    def test_action_plan_type(self):
        actions = [
            IronClawAction(tool="github.summarize_pr", args={"repo": "org/repo", "pr_number": 1}),
        ]
        resp = IronClawResponse(type="action_plan", actions=actions)
        assert resp.type == "action_plan"
        assert len(resp.actions) == 1
        assert resp.actions[0].tool == "github.summarize_pr"


class TestIronClawAction:
    def test_defaults(self):
        action = IronClawAction(tool="test.tool")
        assert action.args == {}
        assert action.description == ""


def _mock_response(status_code: int, json_data: dict) -> httpx.Response:
    """Build an httpx.Response with a request attached so raise_for_status works."""
    request = httpx.Request("POST", "http://test")
    return httpx.Response(status_code, json=json_data, request=request)


def _mock_get_response(status_code: int, json_data: dict) -> httpx.Response:
    request = httpx.Request("GET", "http://test")
    return httpx.Response(status_code, json=json_data, request=request)


class TestIronClawClient:
    @pytest.mark.asyncio
    async def test_interpret_response(self, mock_ironclaw_response):
        client = IronClawClient()

        mock_resp = _mock_response(
            200,
            mock_ironclaw_response(response_type="response", response_text="Done!"),
        )

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.interpret(message="hello", tools=[], context=[])
            assert result.type == "response"
            assert result.response == "Done!"

    @pytest.mark.asyncio
    async def test_interpret_action_plan(self, mock_ironclaw_response):
        client = IronClawClient()

        actions = [{"tool": "slack.send_message", "args": {"channel": "#test", "text": "hi"}}]
        mock_resp = _mock_response(
            200,
            mock_ironclaw_response(response_type="action_plan", actions=actions),
        )

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.interpret(message="send a message", tools=[])
            assert result.type == "action_plan"
            assert len(result.actions) == 1
            assert result.actions[0].tool == "slack.send_message"

    @pytest.mark.asyncio
    async def test_summarize(self):
        client = IronClawClient()

        mock_resp = _mock_response(200, {"summary": "This is a summary."})

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.summarize("Some long content", "Be brief")
            assert result == "This is a summary."

    @pytest.mark.asyncio
    async def test_health_success(self):
        client = IronClawClient()

        mock_resp = _mock_get_response(200, {"status": "healthy"})

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.get.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.health()
            assert result["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_failure(self):
        client = IronClawClient()

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.get.side_effect = httpx.ConnectError("Connection refused")
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.health()
            assert result["status"] == "unreachable"
            assert "error" in result
