# Agent 2: 技术架构调研 — Hermes Agent

## 系统架构概览

Hermes Agent采用**网关-代理（Gateway-Agent）分层架构**：

```
┌─────────────────────────────────────────────────────────┐
│                    Messaging Platforms                    │
│  Telegram │ Discord │ Slack │ WhatsApp │ Signal │ Email  │
│  飞书/Lark │ 企业微信 │ Matrix │ DingTalk │ Webhook     │
└────────────┬────────────────────────────────────────────┘
             │ 统一消息接口
┌────────────▼────────────────────────────────────────────┐
│                    Gateway Process                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Session  │ │ Cron     │ │ Approval │ │ Platform │  │
│  │ Manager  │ │ Scheduler│ │ System   │ │ Adapters │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                     AI Agent Core                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Provider │ │ Context  │ │ Memory   │ │ Skills   │  │
│  │ Router   │ │ Compress │ │ System   │ │ Engine   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Subagent │ │ Plugin   │ │ Tool     │ │ Approval │  │
│  │ Manager  │ │ System   │ │ Executor │ │ Guard    │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                  Terminal Backends                        │
│  Local │ Docker │ SSH │ Singularity │ Daytona │ Modal   │
└─────────────────────────────────────────────────────────┘
```

来源：基于官方README、Release Notes和架构文档的综合分析

---

## 核心子系统详解

### 1. Provider Router（推理提供商路由）

集中式Provider管理，统一`call_llm()`/`async_call_llm()` API。

**支持的Provider（截至v0.8.0）**：

| Provider | 认证方式 | 特殊能力 |
|----------|---------|---------|
| Nous Portal | API Key / OAuth | 400+模型，免费MiMo v2 Pro |
| OpenRouter | API Key | 200+模型，聚合路由 |
| OpenAI / Codex | API Key / OAuth | ChatGPT订阅支持 |
| Anthropic (Claude) | API Key / OAuth PKCE | 原生Prompt缓存，Context Editing API |
| Google AI Studio | API Key | Gemini模型，models.dev自动上下文长度 |
| Hugging Face | API Key | HF Inference API |
| GitHub Copilot | OAuth | 400k上下文 |
| xAI (Grok) | API Key | Prompt缓存 |
| MiniMax | API Key | TTS，Anthropic兼容端点 |
| Kimi/Moonshot | API Key | — |
| z.ai/GLM | API Key | 自动探测端点 |
| Alibaba/DashScope | API Key | 国际端点 |
| Vercel AI Gateway | — | 基础设施级路由 |
| 自定义端点 | API Key / URL | 任意OpenAI兼容端点 |

**关键机制**：
- **Fallback Provider Chain**（v0.6.0+）：有序Provider故障转移链，主Provider失败时自动切换
- **Credential Pool**（v0.7.0+）：同Provider多API Key自动轮换（`least_used`策略），401自动切换
- **Auxiliary Client**：视觉、压缩、子Agent等辅助任务可指定不同Provider
- **Per-turn Primary Restoration**（v0.7.0+）：Fallback使用后下一轮自动恢复主Provider
- **Aggregator-aware Resolution**（v0.8.0+）：优先使用OpenRouter/Nous等聚合Provider

来源：[v0.2.0-v0.8.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

### 2. Learning Loop（学习循环）—— 核心差异化

Hermes Agent的核心创新是内置学习循环，包含四个环节：

```
经验 → 技能创建 → 技能改进 → 知识持久化
  ↑                                    │
  └──────────── 闭环反馈 ←─────────────┘
```

**详细机制**：

| 环节 | 实现方式 | 版本 |
|------|---------|------|
| **技能自动创建** | 复杂任务完成后，Agent自动生成可复用的Skill模板 | v0.2.0+ |
| **技能自我改进** | 技能在使用中根据结果自动优化其流程 | v0.2.0+ |
| **知识持久化** | Agent自动"催促"自己将重要发现写入记忆 | v0.2.0+ |
| **跨会话检索** | FTS5全文搜索 + LLM摘要，搜索历史对话 | v0.2.0+ |
| **用户建模** | Honcho对话式用户建模，理解用户偏好和习惯 | v0.3.0+ |
| **记忆优先级** | 用户偏好和纠正权重高于程序性知识 | v0.3.0+ |
| **可插拔记忆Provider** | ABC基类插件系统，支持自定义记忆后端 | v0.7.0+ |

**Skill系统**：
- 70+内置和可选技能，覆盖15+类别
- Skills Hub社区发现平台
- 兼容agentskills.io开放标准
- 每个平台可独立启用/禁用技能
- 基于工具可用性的条件激活
- 先决条件验证

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）
来源：[v0.2.0, v0.3.0, v0.7.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

### 3. Context Management（上下文管理）

当对话超出模型上下文窗口时，Hermes自动进行上下文压缩：

| 机制 | 说明 | 版本 |
|------|------|------|
| **结构化摘要压缩** | 迭代更新式摘要，保留可操作状态 | v0.4.0重构 |
| **Token预算尾部保护** | 保护最近N轮对话不被压缩 | v0.4.0 |
| **可配置压缩端点** | 可指定压缩使用的模型 | v0.4.0 |
| **比例缩放** | 替代固定token目标，按比例动态调整 | v0.5.0 |
| **防压缩死亡螺旋** | 检测并阻止压缩→失败→再压缩的循环 | v0.7.0 |
| **压缩后状态持久化** | 压缩后立即持久化到网关会话 | v0.7.0 |
| **思考预算耗尽检测** | 模型用尽输出token时跳过无效重试 | v0.5.0 |

来源：[v0.3.0-v0.7.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

### 4. Terminal Backends（终端后端）

六种执行环境，满足从本地开发到云端部署的不同需求：

| 后端 | 适用场景 | 特点 |
|------|---------|------|
| **Local** | 本地开发 | 直接在用户机器上执行 |
| **Docker** | 隔离执行 | 官方Dockerfile，容器加固 |
| **SSH** | 远程服务器 | 持久Shell状态 |
| **Singularity** | HPC环境 | 高性能计算集群 |
| **Daytona** | Serverless开发环境 | 按需唤醒，空闲休眠 |
| **Modal** | Serverless云端 | 原生SDK（v0.5.0重构），RPC脚本 |

**安全机制**：
- Tirith命令审批系统（危险命令需审批）
- 文件系统检查点与回滚
- 命名空间隔离
- 工作目录消毒（v0.8.0）

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）

### 5. Subagent System（子Agent系统）

```
主Agent
├── 子Agent A（独立对话、独立终端、独立工具集）
├── 子Agent B（独立对话、独立终端、独立工具集）
└── 子Agent C（独立对话、独立终端、独立工具集）
```

- 隔离的子Agent实例，各自拥有独立的对话和终端
- Python RPC脚本调用工具，将多步管线压缩为零上下文成本的单轮
- 独立的迭代预算
- 可配置独立的Provider/Model
- 后台任务完成自动通知（v0.8.0）

来源：[v0.2.0, v0.8.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

### 6. Plugin Architecture（插件架构）

```python
# 插件生命周期钩子（v0.5.0+）
pre_llm_call     # LLM调用前
post_llm_call    # LLM调用后
on_session_start # 会话开始
on_session_end   # 会话结束

# v0.8.0扩展
- 注册CLI子命令
- 请求级API钩子（关联ID）
- 安装时提示环境变量
- 会话生命周期事件（finalize/reset）
```

- 将Python文件放入`~/.hermes/plugins/`即可扩展
- 无需Fork项目
- 与MCP互补：MCP提供工具，Plugin提供行为定制

来源：[v0.3.0, v0.5.0, v0.8.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

---

## 数据流

典型请求的数据流路径：

```
用户消息（Telegram/Discord/CLI）
  → Gateway适配器接收
    → Session Manager查找/创建会话
      → Provider Router选择LLM
        → 上下文压缩（如需要）
          → LLM推理（含工具调用）
            → Tool Executor执行
              → Terminal Backend执行命令
            ← 工具结果返回
          ← LLM继续推理
        → 记忆系统更新（异步）
      ← 响应生成
    → 平台适配器格式化
  ← 用户收到回复
```

来源：基于���构文档和Release Notes的综合推断
