"""Session 1.3：跑通第一次模型调用。

运行：
    uv run python -m src.first_call
"""

from __future__ import annotations

import time

import httpx

from src.config import get_settings


def main() -> None:
    settings = get_settings()
    print(f"模型：{settings.model}")
    print(f"端点：{settings.chat_url}\n")

    start = time.perf_counter()
    resp = httpx.post(
        settings.chat_url,
        headers={"Authorization": f"Bearer {settings.api_key}"},
        json={
            "model": settings.model,
            "messages": [{"role": "user", "content": "用一句话解释什么是 AI Agent"}],
        },
        timeout=30.0,
    )
    elapsed = time.perf_counter() - start

    # raise_for_status 是 Go 里 if err != nil 的 Python 版本：
    # 非 2xx 直接抛异常，别默默往下走。
    resp.raise_for_status()
    data = resp.json()

    print("回答：")
    print(data["choices"][0]["message"]["content"])
    print(f"\n耗时：{elapsed:.2f}s")
    print(f"usage：{data.get('usage')}")


if __name__ == "__main__":
    main()
