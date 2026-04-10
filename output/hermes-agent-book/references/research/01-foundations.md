# Agent 1: 基础概念调研 — Hermes Agent

## 核心定义

**Hermes Agent** 是由 **Nous Research** 开发的开源（MIT License）自主AI Agent框架，定位为"The agent that grows with you"（与你共同成长的Agent）。它不是绑定在IDE里的编码副驾驶，也不是单一API的聊天机器人封装——它是一个运行在用户服务器上的自主Agent，具备持久化记忆、自动技能生成和跨平台消息网关能力。

**核心特性**：
- 内置学习循环（Learning Loop）：从经验中创建技能、在使用中改进技能、自动持久化知识
- 跨平台消息网关：Telegram、Discord、Slack、WhatsApp、Signal、Email、CLI、飞书/Lark、企业微信、Matrix、DingTalk、Mattermost、Webhook、Home Assistant
- 多模型支持：Nous Portal、OpenRouter（200+模型）、OpenAI、Anthropic、Google AI Studio、Hugging Face、GitHub Copilot、xAI、MiniMax、Kimi/Moonshot、z.ai/GLM、Alibaba/DashScope等

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手，官方仓库）
来源：[Hermes Agent 官网](https://hermes-agent.nousresearch.com)（一手，官方网站）

---

## 关键术语表

| 英文术语 | 中文翻译 | 定义 |
|---------|---------|------|
| Gateway | 消息网关 | Hermes的中央消息路由进程，将多个即时通讯平台统一接入Agent |
| Skill | 技能 | Agent自主生成或手动创建的流程化任务模板，从经验中提炼 |
| Provider | 推理提供商 | 提供LLM推理服务的平台（如OpenAI、Anthropic、Nous Portal） |
| Terminal Backend | 终端后端 | Agent执行命令的环境，支持local/Docker/SSH/Singularity/Daytona/Modal六种 |
| Subagent | 子Agent | 独立的Agent实例，有自己的对话和终端，用于并行工作 |
| Context Compression | 上下文压缩 | 当对话超出上下文窗口时，自动压缩历史以保留关键信息 |
| Honcho | Honcho记忆系统 | 第三方AI原生跨会话用户建模系统，通过插件集成 |
| MCP (Model Context Protocol) | 模型上下文协议 | Anthropic提出的标准协议，用于扩展Agent工具能力 |
| ACP (Agent Communication Protocol) | Agent通信协议 | 用于IDE（VS Code、Zed、JetBrains）与Agent通信的标准 |
| Credential Pool | 凭证池 | 同一Provider配置多个API Key，自动轮换��故障转移 |
| Profile | 配置文件 | 多实例隔离机制，每个Profile有独立的配置、记忆、会话和网关 |
| Tirith | 安全审批系统 | Hermes的命令审批框架，控制Agent可执行的危险操作 |
| Cron Scheduler | 定时调度器 | 内置的定时任务系统，支持自然语言描述和跨平台投递 |

---

## 发展时间线

| 日期 | 事件 | 意义 |
|------|------|------|
| 2026年3月12日 | **v0.2.0** 发布 | 首个公开标签版本。216个PR，63位贡献者，119个issue。奠定多平台网关、MCP客户端、技能生态、集中式Provider路由、ACP服务器、CLI皮肤引擎、Git Worktree隔离、文件系统检查点等基础能力 |
| 2026年3月17日 | **v0.3.0** 发布 | 流式传输、插件架构、原生Anthropic Provider、智能审批、Honcho记忆、语音模式、持久Shell、Vercel AI Gateway、PII脱敏、Chrome CDP浏览器连接 |
| 2026年3月23日 | **v0.4.0** 发布 | OpenAI兼容API服务器、6个新消息适配器（Signal/DingTalk/SMS/Mattermost/Matrix/Webhook）、4个新推理Provider、MCP服务器管理、@上下文引用、网关Prompt缓存、默认流式传输、200+ bug修复 |
| 2026年3月28日 | **v0.5.0** 发布 | Hugging Face Provider、/model命令重构、Telegram私有聊天话题、原生Modal SDK、插件生命周期钩子、GPT工具使用优化、Nix flake、供应链安全加固、50+安全和可靠性修复 |
| 2026年3月30日 | **v0.6.0** 发布 | Profile多实例、MCP服务器模式、Docker容器、有序Fallback Provider链、飞书/Lark和企业微信支持、Telegram Webhook模式、Slack多工作区OAuth |
| 2026年4月3日 | **v0.7.0** 发布 | 可插拔记忆Provider、同Provider凭证池、Camofox反检测浏览器、内联Diff预览、API服务器会话连续性、客户端提供MCP服务器、网关加固、秘密泄露阻断 |
| 2026年4月8日 | **v0.8.0** 发布 | 后台任务自动通知、免费MiMo v2 Pro、实时模型切换、自优化GPT/Codex指导、原生Google AI Studio、智能不活动超时、审批按钮、MCP OAuth 2.1、集中日志、209个PR、82个issue |

**发展节奏**：从v0.2.0到v0.8.0仅27天，累计1000+个合并PR，覆盖从基础框架到企业级特性的全栈演进。

来源：[Hermes Agent Releases](https://github.com/NousResearch/Hermes-Agent/releases)（一手，官方发布记录）

---

## Nous Research 背景

**Nous Research** 是一家AI研究实验室，以开源大语言模型和Agent框架著称。其代表作品包括：
- **Hermes系列开源模型**（Hermes LLM）——在开源社区广泛使用的指令微调模型
- **Hermes Agent** ——本次调研对象，自改进AI Agent框架
- **Atropos** ——RL训练环境，用于蒸馏Agent策略

Nous Research的核心理念是开源和可访问性，Hermes Agent采用MIT许可证发布。

来源：[Nous Research GitHub](https://github.com/NousResearch)（一手，官方GitHub组织）

---

## 技术定位与分类

Hermes Agent在AI Agent生态中的定位：

| 维度 | Hermes Agent | 编码助手（Cursor/Copilot） | 聊天Agent（ChatGPT） | 自动化Agent（AutoGPT） |
|------|-------------|--------------------------|---------------------|----------------------|
| 运行环境 | 用户服务器/VPS | IDE内 | 云端 | 云端/本地 |
| 记忆 | 持久化+自改进 | 无/有限 | 有（云托管） | 有限 |
| 消息平台 | 15+平台 | IDE内 | Web/App | CLI |
| 模型选择 | 任意（200+） | 绑定 | 绑定 | 有限 |
| 工具执行 | 真实终端+沙箱 | IDE内 | 有限 | 有限 |
| 学习能力 | 内置学习循环 | 无 | 无 | 无 |
| 开源 | MIT | 否 | 否 | 是 |

**核心差异化**：
1. **内置学习循环**——目前唯一声称有built-in learning loop的开源Agent
2. **跨平台消息网关**——不是IDE工具，是服务器端Agent
3. **多模型无锁定**——通过Provider系统实现模型自由切换
4. **六种终端后端**——从本地到云端，从Docker到Modal，灵活部署

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）
来源：[Hermes Agent 官网](https://hermes-agent.nousresearch.com)（一手）
