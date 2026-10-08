"""Session 4：串行 / 全并发 / 限流并发 三组对比实验。

本周的核心交付物。跑完把数据填进 README.md 的「实验数据」章节。

运行：
    uv run python -m src.concurrent_llm
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Coroutine
from dataclasses import dataclass
from typing import Any

import httpx

from src.config import Settings, get_settings

PROMPT = "用一句话解释什么是 AI Agent"
N = 10
CONCURRENCY = 3


@dataclass(frozen=True)
class RunStats:
    """一组实验的结果。"""

    label: str
    elapsed: float
    ok: int
    failed: int
    total_tokens: int

    def row(self) -> str:
        return (
            f"{self.label:<14}{self.elapsed:>8.2f}s"
            f"{self.ok:>6}{self.failed:>6}{self.total_tokens:>9}"
        )


async def call_once(client: httpx.AsyncClient, settings: Settings) -> int:
    """调用一次模型，返回消耗的 token 总数。"""
    resp = await client.post(
        settings.chat_url,
        headers={"Authorization": f"Bearer {settings.api_key}"},
        json={
            "model": settings.model,
            "messages": [{"role": "user", "content": PROMPT}],
        },
    )
    resp.raise_for_status()
    data = resp.json()
    usage: dict[str, Any] = data.get("usage") or {}
    return int(usage.get("total_tokens", 0))


async def run_batch(label: str, tasks: list[Coroutine[Any, Any, int]]) -> RunStats:
    """并发跑一批任务，统计耗时 / 成功 / 失败 / token。

    关键点：return_exceptions=True
    —— 单个任务失败不会拖垮整批。这是 Agent 服务的必备行为，
       第 7 周做生产化时会再遇到它。
    """
    start = time.perf_counter()
    results: list[Any] = await asyncio.gather(*tasks, return_exceptions=True)
    elapsed = time.perf_counter() - start

    ok = sum(1 for r in results if isinstance(r, int))
    failed = len(results) - ok
    tokens = sum(r for r in results if isinstance(r, int))
    return RunStats(label, elapsed, ok, failed, tokens)


async def run_serial(client: httpx.AsyncClient, settings: Settings) -> RunStats:
    """对照组：一次一个，等上一个结束再发下一个。"""
    start = time.perf_counter()
    ok = 0
    failed = 0
    tokens = 0
    for _ in range(N):
        try:
            tokens += await call_once(client, settings)
            ok += 1
        except Exception:  # noqa: BLE001 - 统计用，失败也算数据
            failed += 1
    return RunStats("1. 串行", time.perf_counter() - start, ok, failed, tokens)


async def run_limited(client: httpx.AsyncClient, settings: Settings, limit: int) -> RunStats:
    """生产常用形态：并发 + 限流，防止把上游打挂。"""
    sem = asyncio.Semaphore(limit)

    async def guarded() -> int:
        async with sem:  # 超过 limit 个就排队等
            return await call_once(client, settings)

    return await run_batch(f"3. 限流({limit})", [guarded() for _ in range(N)])


async def main() -> None:
    settings = get_settings()
    limits = httpx.Limits(max_connections=N, max_keepalive_connections=N)

    async with httpx.AsyncClient(timeout=60.0, limits=limits) as client:
        print(f"模型 {settings.model}，共 {N} 次调用\n")

        stats = [
            await run_serial(client, settings),
            await run_batch("2. 全并发", [call_once(client, settings) for _ in range(N)]),
            await run_limited(client, settings, CONCURRENCY),
        ]

    header = f"{'模式':<12}{'耗时':>10}{'成功':>6}{'失败':>6}{'tokens':>9}"
    print(header)
    print("-" * len(header))
    for s in stats:
        print(s.row())

    print("\n把上面这张表填进 README.md 的「实验数据」章节。")
    print("思考题：为什么限流版的耗时介于串行和全并发之间？")


if __name__ == "__main__":
    asyncio.run(main())
