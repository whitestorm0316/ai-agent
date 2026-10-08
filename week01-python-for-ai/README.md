# week01 · Python for AI 速成（Go 开发者视角）

> 第 1 周：能用 Python 写出并发调用大模型 API 的代码，并彻底搞懂 asyncio 和 goroutine 的区别。
>
> 详细任务拆解见 [`../docs/03-第1周详细计划-Python-for-AI速成.html`](../docs/03-第1周详细计划-Python-for-AI速成.html)
>
> 两台电脑的全局工作流见 [根目录 README](../README.md)

---

## 一、首次配置（每台电脑一次）

```bash
cd week01-python-for-ai
./bootstrap.sh          # 装 uv、装依赖、生成 .env、跑一遍测试
# 然后编辑 .env 填入 LLM_API_KEY
```

---

## 二、常用命令

```bash
make setup    # 安装依赖（首次或换电脑）
make check    # 格式化 + lint + 类型检查 + 测试 ← 提交前跑这个
make fmt      # 只格式化
make lint     # 只 lint
make type     # 只类型检查
make test     # 只跑测试（不联网、不花钱）
make exp      # Session 3 实验：阻塞 vs 异步（不花钱）
make run      # Session 4 实验：串行/并发/限流（消耗额度）
make clean    # 清理缓存
```

给 Go 开发者的对照：

| 本目录 | Go 生态 |
| --- | --- |
| `pyproject.toml` | `go.mod` |
| `uv.lock` | `go.sum` |
| `.python-version` | `go` 指令版本 |
| `uv sync` | `go mod download` |
| `ruff format` / `ruff check` | `gofmt` / `go vet` |
| `mypy .` | 编译期类型检查 |
| `pytest` | `go test` |

---

## 三、目录结构

```
week01-python-for-ai/
├── .env.example              # 配置模板（.env 不进仓库）
├── .gitignore
├── .python-version           # 锁定 Python 3.12，保证两台电脑一致
├── Makefile                  # 常用命令入口
├── README.md
├── NOTES.md                  # 本周学习笔记 / 踩坑记录
├── bootstrap.sh              # 换电脑一键初始化
├── pyproject.toml            # ≈ go.mod
├── src/
│   ├── config.py             # 集中读配置，缺 key 直接报错
│   ├── first_call.py         # Session 1.3 第一次调用
│   ├── tools.py              # Session 2.3 / 5.1 工具 Schema（第 2 周复用）
│   ├── concurrent_llm.py     # Session 4 并发调用 + 三组对比
│   └── experiments/
│       ├── blocking_vs_async.py      # 实验 A/B：time.sleep vs asyncio.sleep
│       └── sync_vs_async_http.py     # 实验 C/D：同步 vs 异步 HTTP
└── tests/
    ├── test_tools.py                 # Schema 结构 + description 完整性
    └── test_concurrent_llm.py        # 单个失败不拖垮整批
```

---

## 四、实验数据（跑完填这里）

### Session 3：阻塞 vs 异步（`make exp`）

| 实验 | 写法 | 耗时 |
| --- | --- | --- |
| A | `time.sleep(3)` × 5 | |
| B | `await asyncio.sleep(3)` × 5 | |
| C | 同步 HTTP × 5 | |
| D | 异步 HTTP × 5 | |

> 参考值：在本机实测 A = 15.02s，B = 3.00s，差 5 倍。

### Session 4：串行 / 并发 / 限流（`make run`）

| 模式 | 耗时 | 成功 | 失败 | tokens |
| --- | --- | --- | --- | --- |
| 1. 串行 | | | | |
| 2. 全并发 | | | | |
| 3. 限流(3) | | | | |

**思考题：**

1. 为什么限流版的耗时介于串行和全并发之间？
2. `asyncio.Semaphore` 限流和 `httpx.Limits` 连接池，分别控制什么？
3. 如果某个请求返回 500，`return_exceptions=True` 在这里起了什么作用？

---

## 五、本周进度

- [ ] Session 1：环境与工具链，跑通第一次调用
- [ ] Session 2：语法差异 + Pydantic，`src/tools.py` 就绪
- [ ] Session 3：asyncio 心智模型，四个实验都跑过
- [ ] Session 4：并发调用 + 三组对比数据填进上表
- [ ] Session 5：10 道自测题全过，笔记写进 `NOTES.md`
- [ ] 出关：`make check` 全绿，`src/tools.py` 可供第 2 周直接 import

---

## 六、排错

**`缺少 LLM_API_KEY`**
还没建 `.env`。执行 `cp .env.example .env` 并填入 key。

**`uv: command not found`**
`curl -LsSf https://astral.sh/uv/install.sh | sh`，然后重开终端，或 `export PATH="$HOME/.local/bin:$PATH"`。

**mypy 报一堆错**
第一次跑 mypy strict 一定会报错，这是正常的。逐条修，修完你会感谢自己——这正是 Go 编译期检查的等价物。真觉得 ANN 规则太吵，可以改 `pyproject.toml` 里的 `select`。

**`.env` 不小心提交了**
立刻去服务商后台吊销这个 key，重新生成。然后用 `git rm --cached .env` 把它从版本控制里移除。
