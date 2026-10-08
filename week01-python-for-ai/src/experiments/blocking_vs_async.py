"""Session 3.3 实验 A / B：同步阻塞 vs 异步等待。

这是本周最重要的实验。做完你会明白：
asyncio 不是"更轻的线程"，而是"一个线程 + 一个事件循环 + 一堆可暂停的函数"。
任何一处同步阻塞，会让整个事件循环停摆。

运行：
    uv run python -m src.experiments.blocking_vs_async
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable

TASKS = 5
SLEEP = 3.0

TaskFn = Callable[[int], Awaitable[int]]


async def blocking_task(i: int) -> int:
    """❌ 反面教材：同步 sleep 会卡死整个事件循环。"""
    time.sleep(SLEEP)
    return i


async def async_task(i: int) -> int:
    """✅ 正确写法：await 时让出控制权，其他协程可以继续跑。"""
    await asyncio.sleep(SLEEP)
    return i


async def measure(label: str, task_fn: TaskFn) -> float:
    start = time.perf_counter()
    await asyncio.gather(*(task_fn(i) for i in range(TASKS)))
    elapsed = time.perf_counter() - start
    print(f"{label:<28} {TASKS} 个任务 耗时 {elapsed:5.2f}s")
    return elapsed


async def main() -> None:
    print(f"每个任务 sleep {SLEEP}s，并发 {TASKS} 个\n")

    bad = await measure("A. time.sleep（同步阻塞）", blocking_task)
    good = await measure("B. await asyncio.sleep（异步）", async_task)

    print(f"\n结论：理论上限是 {SLEEP:.1f}s，实际差了 {bad / good:.1f} 倍。")
    print("→ 在 async 函数里写同步阻塞调用，并发能力直接归零。")


if __name__ == "__main__":
    asyncio.run(main())
