"""并发批量执行的测试。

这里刻意不调真实模型——测试应该离线可跑、不烧钱。
做法是把 run_batch 当成纯函数来测：喂它一批假的协程，验证统计逻辑。
"""

import asyncio

from src.concurrent_llm import run_batch


async def _ok() -> int:
    await asyncio.sleep(0.01)
    return 100


async def _boom() -> int:
    raise RuntimeError("模拟工具调用失败")


async def test_all_success() -> None:
    stats = await run_batch("test", [_ok(), _ok(), _ok()])
    assert stats.ok == 3
    assert stats.failed == 0
    assert stats.total_tokens == 300


async def test_single_failure_does_not_kill_batch() -> None:
    """这是本周最该守住的行为：一个失败不能拖垮整批。"""
    stats = await run_batch("test", [_ok(), _boom(), _ok()])
    assert stats.ok == 2
    assert stats.failed == 1
    assert stats.total_tokens == 200


async def test_concurrency_actually_overlaps() -> None:
    """三个 0.2s 的任务并发跑，总耗时应该明显小于 0.6s。"""

    async def slow() -> int:
        await asyncio.sleep(0.2)
        return 1

    stats = await run_batch("test", [slow(), slow(), slow()])
    assert stats.elapsed < 0.5
