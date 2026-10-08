"""Session 3.3 实验 C / D：同步 requests vs 异步 httpx。

同样的并发逻辑，换掉 HTTP 客户端，性能差好几倍。
这个实验不消耗模型额度，只打公开的测试接口。

运行：
    uv run python -m src.experiments.sync_vs_async_http
"""

from __future__ import annotations

import asyncio
import time

import httpx

URL = "https://httpbin.org/delay/1"
N = 5


def sync_fetch(i: int) -> int:
    """❌ 同步 requests 风格：一个请求结束才能发下一个。"""
    resp = httpx.get(URL, timeout=30.0)
    return resp.status_code


async def async_fetch(client: httpx.AsyncClient, i: int) -> int:
    """✅ 异步：await 时让出控制权，其他请求同时进行。"""
    resp = await client.get(URL)
    return resp.status_code


async def main() -> None:
    print(f"目标 {URL}，每个请求约 1s，并发 {N} 个\n")

    start = time.perf_counter()
    for i in range(N):
        sync_fetch(i)
    sync_elapsed = time.perf_counter() - start
    print(f"{'C. 同步 httpx.get':<26} 耗时 {sync_elapsed:5.2f}s")

    start = time.perf_counter()
    limits = httpx.Limits(max_connections=N, max_keepalive_connections=N)
    async with httpx.AsyncClient(timeout=30.0, limits=limits) as client:
        await asyncio.gather(*(async_fetch(client, i) for i in range(N)))
    async_elapsed = time.perf_counter() - start
    print(f"{'D. 异步 AsyncClient':<26} 耗时 {async_elapsed:5.2f}s")

    print(f"\n差了 {sync_elapsed / async_elapsed:.1f} 倍。")
    print("→ 注意：这里同步版用了 httpx.get，换成 requests.get 结果一样，")
    print("  因为问题不在库，在于'同步调用会阻塞事件循环'这件事本身。")


if __name__ == "__main__":
    asyncio.run(main())
