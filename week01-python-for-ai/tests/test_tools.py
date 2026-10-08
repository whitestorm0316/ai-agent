"""工具 Schema 的测试。

原则：测试不依赖网络、不消耗模型额度。
"""

from src.tools import get_tool_schemas


def test_schema_shape() -> None:
    schemas = get_tool_schemas()
    assert len(schemas) == 3
    for s in schemas:
        assert s["type"] == "function"
        fn = s["function"]
        assert fn["name"]
        assert fn["description"]
        assert fn["parameters"]["type"] == "object"
        # 顶层 title 已被清理掉，模型侧不需要
        assert "title" not in fn["parameters"]


def test_weather_schema_required_and_description() -> None:
    schema = next(s for s in get_tool_schemas() if s["function"]["name"] == "get_weather")
    params = schema["function"]["parameters"]
    assert params["required"] == ["city"]
    assert "深圳" in params["properties"]["city"]["description"]


def test_every_field_has_description() -> None:
    """description 是写给模型看的，缺了会显著降低工具调用准确率。"""
    for s in get_tool_schemas():
        tool_name = s["function"]["name"]
        for field_name, prop in s["function"]["parameters"]["properties"].items():
            assert prop.get("description"), f"{tool_name}.{field_name} 缺少 description"
