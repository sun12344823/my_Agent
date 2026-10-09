# my-agent 🤖

> 从 0 开始亲手构建的轻量级智能体框架 —— 学习自《Hello-Agents》第七章「构建你的智能体框架」
> 学习方式：每课一个 commit，在 git log 里留下完整的构建轨迹

## 为什么自己写框架？

- **深度理解原理**：穿透 LangChain 等框架的抽象，看清 Agent 循环的本质
- **完全控制权**：每一行代码都是自己的，可精确调优
- **系统设计训练**：分层解耦、接口抽象、错误处理的软件工程实战

## 架构

```
my_agent/
├── core/                  # 核心层（不依赖其他自研模块）
│   ├── llm.py             # 统一 LLM 接口（多 provider + 自动检测）
│   ├── message.py         # Message 消息类
│   ├── config.py          # Config 配置类
│   ├── agent.py           # Agent 抽象基类
│   └── exceptions.py      # 异常体系
├── agents/                # Agent 实现层（依赖 core）
│   ├── simple_agent.py    # 对话 + 文本协议工具调用
│   ├── react_agent.py     # ReAct 范式
│   ├── reflection_agent.py
│   └── plan_solve_agent.py
└── tools/                 # 工具系统层
    ├── base.py            # Tool 基类 + ToolParameter
    ├── registry.py        # ToolRegistry 注册表
    └── builtin/           # 内置工具（计算器等）
```

## 快速开始

```bash
# 1. 安装（需要 Python 3.10+）
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. 配置
cp .env.example .env   # 填入你的 API Key

# 3. 运行
python examples/01_basic_chat.py
```

## 课程进度

- [x] 第 0 课：环境与仓库初始化
- [ ] 第 1 课：统一 LLM 接口 `core/llm.py`
- [ ] 第 2 课：Message / Config / Agent 基类
- [ ] 第 3 课：工具系统 Tool / ToolRegistry
- [ ] 第 4 课：SimpleAgent
- [ ] 第 5 课：ReActAgent
- [ ] 第 6 课：ReflectionAgent + PlanAndSolveAgent
- [ ] 第 7 课：FunctionCallAgent（原生函数调用）
- [ ] 第 8 课：多源搜索工具 + 工具链
- [ ] 第 9 课：端到端 demo 与收尾

## 教学笔记

（每课学完后在这里记录心得）

## License

MIT
