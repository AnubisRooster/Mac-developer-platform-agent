"""Unit tests for tools.registry.ToolRegistry."""

from tools.registry import ToolRegistry, ToolSchema


class TestToolRegistry:
    def test_register_and_list(self, sample_tool_func):
        reg = ToolRegistry()
        reg.register("slack.send_message", sample_tool_func, "Send message")
        assert "slack.send_message" in reg.list_tools()

    def test_get_handler(self, sample_tool_func):
        reg = ToolRegistry()
        reg.register("test.tool", sample_tool_func, "A test tool")
        handler = reg.get_handler("test.tool")
        assert handler is sample_tool_func

    def test_get_handler_missing(self):
        reg = ToolRegistry()
        assert reg.get_handler("nonexistent") is None

    def test_get_schema(self, sample_tool_func):
        params = {"type": "object", "properties": {"channel": {"type": "string"}}}
        reg = ToolRegistry()
        reg.register("test.tool", sample_tool_func, "A tool", params)
        schema = reg.get_schema("test.tool")
        assert schema is not None
        assert schema.name == "test.tool"
        assert schema.description == "A tool"
        assert schema.parameters == params

    def test_get_schema_missing(self):
        reg = ToolRegistry()
        assert reg.get_schema("nonexistent") is None

    def test_get_all_schemas(self, sample_tool_func):
        reg = ToolRegistry()
        reg.register("a.tool", sample_tool_func, "Tool A")
        reg.register("b.tool", sample_tool_func, "Tool B")
        schemas = reg.get_all_schemas()
        assert len(schemas) == 2
        names = {s["name"] for s in schemas}
        assert names == {"a.tool", "b.tool"}

    def test_get_tool_descriptions(self, sample_tool_func):
        reg = ToolRegistry()
        reg.register("test.tool", sample_tool_func, "A test tool")
        desc = reg.get_tool_descriptions()
        assert "test.tool" in desc
        assert "A test tool" in desc

    def test_empty_descriptions(self):
        reg = ToolRegistry()
        assert reg.get_tool_descriptions() == "No tools registered."


class TestToolSchema:
    def test_schema_defaults(self):
        schema = ToolSchema(name="test", description="desc")
        assert schema.parameters == {}

    def test_schema_with_params(self):
        params = {"type": "object", "properties": {"x": {"type": "integer"}}}
        schema = ToolSchema(name="test", description="desc", parameters=params)
        assert schema.parameters["type"] == "object"
