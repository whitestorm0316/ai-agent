.PHONY: help setup check fmt lint type test run exp clean

help:
	@echo "make setup   安装依赖（首次或换了电脑）"
	@echo "make check   格式化 + lint + 类型检查 + 测试（提交前跑这个）"
	@echo "make fmt     只格式化"
	@echo "make lint    只 lint（自动修可修的）"
	@echo "make type    只类型检查"
	@echo "make test    只跑测试"
	@echo "make exp     跑 Session 3 的阻塞实验（不花钱）"
	@echo "make run     跑 Session 4 的并发调用实验（会消耗额度）"
	@echo "make clean   清理缓存"

setup:
	uv sync

check: fmt lint type test

fmt:
	uv run ruff format .

lint:
	uv run ruff check . --fix

type:
	uv run mypy .

test:
	uv run pytest -q

exp:
	uv run python -m src.experiments.blocking_vs_async
	uv run python -m src.experiments.sync_vs_async_http

run:
	uv run python -m src.concurrent_llm

clean:
	rm -rf .ruff_cache .mypy_cache .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
