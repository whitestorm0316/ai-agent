# 第 1 周笔记

## 一句话总结本周

<!-- 例：asyncio 不是"更轻的线程"，而是"一个线程 + 一个事件循环 + 一堆可暂停的函数"。 -->

## Go → Python 踩坑记录

<!-- Session 5 的任务：整理成《Go 开发者踩的 5 个 Python 坑》，发到掘金或博客 -->

1.
2.
3.
4.
5.

## 自测题答案（凭记忆写，别抄）

1. `pyproject.toml` / `uv.lock` / `.venv` 分别对应 Go 里的什么？
2. type hints 在运行时会被强制检查吗？谁负责检查？
3. `model_json_schema()` 的输出有什么用？和 function calling 什么关系？
4. goroutine 和 asyncio 协程最本质的区别是什么？
5. 在 async 函数里调用 `requests.get()` 会发生什么？为什么？
6. `asyncio.gather` 相当于 Go 里的什么？
7. 怎么把并发数限制在 5 以内？
8. `asyncio.create_task()` 之后为什么必须持有返回值的引用？
9. 忘记写 `await` 会怎样？会报错吗？
10. Python 有 GIL，为什么 Agent 服务里还要用多进程？

## 待解决 / 还没搞懂的问题

<!-- 留着，第 2 周带着问题继续 -->

-
