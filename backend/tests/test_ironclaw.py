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
            assert result.actions[0].args["channel"] == "#test"

    @pytest.mark.asyncio
    async def test_interpret_passes_tools_as_openai_format(self):
        client = IronClawClient()

        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
        })

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            tools = [{"name": "test.tool", "description": "A test tool", "parameters": {"type": "object"}}]
            await client.interpret(message="test", tools=tools)

            call_args = mock_instance.post.call_args
            payload = call_args.kwargs.get("json") or call_args[1].get("json")
            assert "tools" in payload
            assert payload["tools"][0]["type"] == "function"
            assert payload["tools"][0]["function"]["name"] == "test.tool"

    @pytest.mark.asyncio
    async def test_summarize(self):
        client = IronClawClient()

        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "This is a summary."}, "finish_reason": "stop"}],
        })

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

        mock_resp = _mock_get_response(200, {
            "data": [{"id": "qwen3.5:latest", "object": "model", "created": 0, "owned_by": "ironclaw"}],
            "object": "list",
        })

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.get.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            result = await client.health()
            assert result["status"] == "connected"
            assert "qwen3.5:latest" in result["models"]

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

    @pytest.mark.asyncio
    async def test_auth_header_sent(self):
        client = IronClawClient()
        client._auth_token = "test-token"

        mock_resp = _mock_response(200, {
            "id": "chatcmpl-test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
        })

        with patch("agent.ironclaw.httpx.AsyncClient") as mock_cls:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_resp
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_instance

            await client.interpret(message="test", tools=[])

            call_args = mock_instance.post.call_args
            headers = call_args.kwargs.get("headers") or call_args[1].get("headers")
            assert headers["Authorization"] == "Bearer test-token"
