"""集中读取配置。

Go 里你可能会写一个 config 包 + 一个 Settings struct，这里思路一样。
关键差异：Python 没有编译期强制，所以这里做运行期校验，缺 key 直接报错。
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """模型服务配置。换厂商只需改 .env，不用改代码。"""

    api_key: str
    base_url: str
    model: str

    @property
    def chat_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


def get_settings() -> Settings:
    """从环境变量读取配置，缺失则立刻报错（fail fast）。"""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    if not api_key or api_key.startswith("sk-在这里填"):
        raise RuntimeError(
            "缺少 LLM_API_KEY。\n请先执行：cp .env.example .env，然后编辑 .env 填入你的 key。"
        )
    return Settings(
        api_key=api_key,
        base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
        model=os.environ.get("LLM_MODEL", "deepseek-chat"),
    )
