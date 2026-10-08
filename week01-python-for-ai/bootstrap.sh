#!/usr/bin/env bash
# 第二台电脑一键初始化。clone 之后跑一次即可。
set -euo pipefail

echo "==> 检查 uv"
if ! command -v uv >/dev/null 2>&1; then
  echo "    未安装，正在安装 uv ..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
echo "    $(uv --version)"

echo "==> 安装依赖（uv 会自动准备 .python-version 指定的 Python）"
uv sync

echo "==> 检查 .env"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "    已从 .env.example 生成 .env —— 请编辑它填入你的 LLM_API_KEY"
else
  echo "    .env 已存在，跳过"
fi

echo "==> 跑一遍测试（不联网，验证环境正常）"
uv run pytest -q

cat <<'TIP'

完成。接下来：
  1) 编辑 .env 填入 LLM_API_KEY
  2) make check     # 格式化 + lint + 类型检查 + 测试
  3) make exp       # Session 3 实验（不花钱）
  4) make run       # Session 4 并发实验（消耗额度）

TIP
