"""Session 2.3 / 5.1：工具 Schema 定义。

Pydantic 在 AI 生态里的地位 ≈ Go 的 struct tag + 校验库。
这里定义的每个字段，最终都会变成模型看到的工具参数说明——
所以 description 是写给"模型"看的，不是写给同事看的，要写得具体。

第 2 周手写 Function Calling 时，直接 import get_tool_schemas()。

运行自检：
    uv run python -m src.tools
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field


class WeatherArgs(BaseModel):
    """查询指定城市的当前天气。"""

    city: str = Field(description="城市名称，例如：深圳")
    unit: str = Field(default="celsius", description="温度单位，celsius 或 fahrenheit")


class CalculatorArgs(BaseModel):
    """计算一个数学表达式。"""

    expression: str = Field(description="要计算的数学表达式，例如：(12 + 5) * 3")


class ReadFileArgs(BaseModel):
    """读取本地文本文件的内容。"""

    path: str = Field(description="文件的相对路径，例如：README.md")
    max_bytes: int = Field(default=4096, description="最多读取的字节数")


TOOL_REGISTRY: dict[str, type[BaseModel]] = {
    "get_weather": WeatherArgs,
    "calculate": CalculatorArgs,
    "read_file": ReadFileArgs,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "get_weather": "查询指定城市的当前天气",
    "calculate": "计算一个数学表达式",
    "read_file": "读取本地文本文件的内容",
}


def _clean_schema(model: type[BaseModel]) -> dict[str, Any]:
    """去掉顶层 title，让 schema 更干净（模型侧不需要它）。"""
    schema = model.model_json_schema()
    schema.pop("title", None)
    return schema


def get_tool_schemas() -> list[dict[str, Any]]:
    """导出 OpenAI function calling 格式的工具定义列表。"""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": TOOL_DESCRIPTIONS[name],
                "parameters": _clean_schema(model),
            },
        }
        for name, model in TOOL_REGISTRY.items()
    ]


def _demo() -> None:
    schemas = get_tool_schemas()
    print(json.dumps(schemas, ensure_ascii=False, indent=2))
    print(f"\n共 {len(schemas)} 个工具。")


if __name__ == "__main__":
    _demo()
