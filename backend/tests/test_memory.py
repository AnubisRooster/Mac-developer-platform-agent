"""Unit tests for agent.memory.ConversationMemory."""

from agent.memory import ConversationMemory


class TestConversationMemory:
    def test_empty_on_init(self):
        mem = ConversationMemory()
        assert mem.get_context() == []
        assert mem.get_summary() == "No messages yet."

    def test_add_and_retrieve(self):
        mem = ConversationMemory()
        mem.add_message("user", "hello")
        mem.add_message("assistant", "hi there")

        ctx = mem.get_context()
        assert len(ctx) == 2
        assert ctx[0]["role"] == "user"
        assert ctx[0]["content"] == "hello"
        assert ctx[1]["role"] == "assistant"

    def test_context_limit(self):
        mem = ConversationMemory()
        for i in range(30):
            mem.add_message("user", f"msg-{i}")
        ctx = mem.get_context(max_messages=5)
        assert len(ctx) == 5
        assert ctx[0]["content"] == "msg-25"

    def test_to_llm_messages(self):
        mem = ConversationMemory()
        mem.add_message("user", "question")
        mem.add_message("assistant", "answer")

        msgs = mem.to_llm_messages()
        assert len(msgs) == 2
        assert set(msgs[0].keys()) == {"role", "content"}
        assert "timestamp" not in msgs[0]

    def test_clear(self):
        mem = ConversationMemory()
        mem.add_message("user", "hello")
        mem.clear()
        assert mem.get_context() == []

    def test_summary(self):
        mem = ConversationMemory()
        mem.add_message("user", "a")
        mem.add_message("assistant", "b")
        mem.add_message("user", "c")
        summary = mem.get_summary()
        assert "3 messages" in summary
        assert "2 from user" in summary
