# AI Agent 转行计划

> 从 Go 后端到深圳 AI Agent 岗位 · 11 周学习项目
>
> 文档与代码同仓管理。两台电脑交替开发，随时 `git pull` 接着干。

---

## 一、这个仓库是什么

一个自用的转行学习项目，三部分内容放在一起：

| 部分 | 位置 | 说明 |
| --- | --- | --- |
| **调研** | `docs/01-*` | 深圳 AI Agent 岗位到底要什么能力（基于 790+ 在招职位） |
| **路线** | `docs/02-*` | 11 周学习计划，针对 Go 开发者定制 |
| **代码** | `weekNN-*/` | 每周一个独立可运行子项目 |

文档是 HTML，用浏览器打开即可（也可在编辑器的预览里看）。

---

## 二、目录结构

```
.
├── README.md                      ← 你在这里
├── .gitattributes                 ← 统一换行符
├── .gitignore
├── docs/                          ← 调研与计划文档
│   ├── 01-深圳AI-Agent岗位调研报告.html
│   ├── 02-学习路线-Go开发者版-11周.html
│   ├── 03-第1周详细计划-Python-for-AI速成.html
│   └── archive/                   ← 已作废的版本，仅留档
└── week01-python-for-ai/          ← 第 1 周：Python for AI 速成
    ├── README.md                  ← 本周详细说明
    ├── NOTES.md                   ← 学习笔记 / 踩坑记录
    ├── Makefile
    ├── bootstrap.sh
    ├── pyproject.toml
    ├── src/
    └── tests/
```

### 每周目录约定

以后每周新增一个 `weekNN-<主题>/` 目录，**各自是独立的 uv 项目**（自己一份 `pyproject.toml` + `uv.lock`），互不干扰。命名示例：

```
week01-python-for-ai/
week02-llm-and-function-calling/
week03-04-rag-pipeline/
week05-06-langgraph-and-mcp/
week07-08-production-and-eval/
week09-10-multi-agent-project/
```

每新增一周，在下面第三节的进度表里打勾。

---

## 三、11 周进度

| 周次 | 主题 | 代码目录 | 状态 |
| --- | --- | --- | --- |
| 1 | Python for AI 速成（Go 视角） | `week01-python-for-ai/` | 🚧 进行中 |
| 2 | LLM 语义层 + 手写 Function Calling | — | ⬜ |
| 3–4 | RAG 全链路 + 评估体系 | — | ⬜ |
| 5–6 | LangGraph 编排 + MCP 双通道 | — | ⬜ |
| 7–8 | 生产化 + 可观测性 + 记忆 | — | ⬜ |
| 9–10 | 项目二 + 双栈作品集 | — | ⬜ |
| 11 | 面试冲刺 + 投递 | — | ⬜ |

> 状态标记：⬜ 未开始 · 🚧 进行中 · ✅ 已完成

---

## 四、两台电脑怎么用

### 第一次：在电脑 A 上推到远端

先在 GitHub 或 Gitee 建一个**空仓库**（不要勾选自动生成 README），然后：

```bash
# 在仓库根目录（就是有这个 README 的那一层）
git remote add origin <你的仓库地址>

# 示例：
#   Gitee : git@gitee.com:<用户名>/ai-agent-roadmap.git
#   GitHub: git@github.com:<用户名>/ai-agent-roadmap.git

git push -u origin main
```

### 第一次：在电脑 B 上接上

```bash
git clone <你的仓库地址> ai-agent-roadmap
cd ai-agent-roadmap/week01-python-for-ai
./bootstrap.sh          # 装 uv、装依赖、生成 .env、跑一遍测试
```

然后编辑 `.env` 填入自己的 API Key。

> **注意：每一周目录都要单独 `bootstrap.sh`**，因为每周是独立的 uv 项目。

### 日常节奏（两台电脑一样）

```bash
# 开工前 —— 先同步
git pull --rebase

# ... 写代码、做实验 ...

# 收工前 —— 提交并推送
cd week01-python-for-ai && make check    # 先过质量门禁
cd .. && git add -A
git commit -m "week1: 完成 asyncio 实验"
git push
```

**切电脑前必须 push。** 这是唯一规则。

---

## 五、每台电脑只需配置一次

### Git 身份

```bash
git config --global user.name  "你的名字"
git config --global user.email "你的邮箱"
```

### SSH Key（免密推送，两台机器各配一次）

```bash
ssh-keygen -t ed25519 -C "你的邮箱"     # 一路回车
pbcopy < ~/.ssh/id_ed25519.pub          # macOS 复制公钥
# 粘贴到 GitHub / Gitee 的 SSH Keys 设置页
ssh -T git@gitee.com                    # 验证
```

### API Key

在**每个周目录**下：

```bash
cp .env.example .env
# 编辑 .env，填入 LLM_API_KEY
```

`.env` 已被 `.gitignore` 忽略。**两台电脑各存一份，不要提交，不要发群里。**

---

## 六、文档索引

| 文档 | 内容 | 什么时候看 |
| --- | --- | --- |
| [01-深圳AI-Agent岗位调研报告](docs/01-深圳AI-Agent岗位调研报告.html) | 790+ 岗位的能力要求统计、薪资分布、真实 JD 拆解、面试考点 | 想知道「市场要什么」时 |
| [02-学习路线-Go开发者版-11周](docs/02-学习路线-Go开发者版-11周.html) | 11 周总计划、Go→Python 迁移地图、技术栈选型、项目设计 | 想知道「整体怎么走」时 |
| [03-第1周详细计划](docs/03-第1周详细计划-Python-for-AI速成.html) | 5 个 session 的逐项任务、可运行代码、10 道自测题 | 做第 1 周时对着看 |

---

## 七、排错

**`uv: command not found`**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 重开终端，或：
export PATH="$HOME/.local/bin:$PATH"
```

**`缺少 LLM_API_KEY`**

对应周目录下还没建 `.env`。执行 `cp .env.example .env` 并填入 key。

**两台电脑 Python 版本不一致**

不要手动改。各周的 `.python-version` 已锁定版本，`uv sync` 会自动准备对应解释器。

**`.env` 不小心提交了**

立刻去服务商后台吊销这个 key 并重新生成，然后：

```bash
git rm --cached week01-python-for-ai/.env
```

**Pull 时提示冲突**

说明两台电脑都改了同一处。`.gitattributes` 已经让 `uv.lock` 不参与行合并，如果仍冲突，最简单的做法是接受远端版本后重新 `uv sync` 生成锁文件。
