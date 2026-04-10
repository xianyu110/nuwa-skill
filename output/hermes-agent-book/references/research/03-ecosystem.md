# Agent 3: 生态调研 — Hermes Agent

## GitHub项目数据

| 指标 | 数据 | 备注 |
|------|------|------|
| Stars | 43,212 | 高热度开源项目 |
| Forks | 5,519 | 活跃的社区参与 |
| Open Issues | 2,433 | 快速迭代但Issue积压明显 |
| Contributors | 63+（v0.2.0时） | 快速增长的贡献者群体 |
| 许可证 | MIT | 完全开放 |
| 开发语言 | Python | 主要语言 |
| 首次公开 | 2026年3月12日（v0.2.0） | 至今不到1个月 |
| 最新版本 | v0.8.0（2026年4月8日） | 27天内7个版本 |
| 累计合并PR | 1000+ | 极高的开发活跃度 |

来源：[GitHub仓库](https://github.com/NousResearch/Hermes-Agent)（一手）
来源：[v0.2.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

---

## 安装方式

### 一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

支持Linux、macOS、WSL2。安装器自动处理Python、Node.js、依赖和`hermes`命令。Windows需要WSL2。

### 开发安装

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
```

### Docker部署

```bash
# v0.6.0+ 提供官方Dockerfile
# 支持CLI和Gateway模式，配置通过volume挂载
```

### Nix安装

```bash
# v0.5.0+ 提供Nix flake
# 包含NixOS模块，支持持久化容器模式
```

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手，官方安装文档）

---

## CLI命令体系

| 命令 | 功能 | 说明 |
|------|------|------|
| `hermes` | 交互式CLI | 启动TUI对话 |
| `hermes model` | 模型管理 | 选择/切换LLM Provider和模型 |
| `hermes tools` | 工具配置 | 启用/禁用工具集 |
| `hermes config set` | 配置管理 | 设置配置项 |
| `hermes setup` | 设置向导 | 一站式配置 |
| `hermes gateway` | 消息网关 | 启动多平台消息网关 |
| `hermes update` | 更新 | 更新到最新版本 |
| `hermes doctor` | 诊断 | 检测问题 |
| `hermes logs` | 日志 | 查看/过滤日志（v0.8.0） |
| `hermes profile` | 多实例管理 | 创建/切换/导出Profile（v0.6.0） |
| `hermes mcp` | MCP管理 | 安装/配置/认证MCP服务器（v0.4.0） |
| `hermes mcp serve` | MCP服务器模式 | 将Hermes暴露为MCP服务（v0.6.0） |
| `hermes claw migrate` | 迁移 | 从OpenClaw导入设置 |

### 会话内斜杠命令

| 命令 | 功能 |
|------|------|
| `/new` / `/reset` | 新建会话 |
| `/model [provider:model]` | 切换模型（v0.8.0全平台支持） |
| `/retry` / `/undo` | 重试/撤销 |
| `/compress` | 手动压缩上下文 |
| `/usage` / `/insights` | 用量统计 |
| `/skills` | 浏览技能 |
| `/stop` | 中断当前执行 |
| `/browser` | 交互式浏览器 |
| `/personality` | 设置人格 |
| `/reasoning` | 推理力度控制 |
| `/approve` / `/deny` | 审批/拒绝危险命令 |
| `/queue` | 队列提示 |
| `/cost` | 实时定价追踪 |

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）
来源：[v0.4.0, v0.5.0, v0.8.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

---

## Skills生态系统

### 内置技能

70+内置和可选技能，覆盖15+类别：
- 代码开发（代码生成、调试、重构）
- 文件操作（搜索、编辑、转换）
- 网络操作（搜索、爬取、API调用）
- 系统管理（进程、服务、备份）
- 数据分析（统计、可视化）
- 写作辅助（文档、翻译、摘要）

### Skills Hub

社区技能发现平台，用户可以：
- 浏览社区贡献的技能
- 一键安装第三方技能
- 分享自己创建的技能

### agentskills.io兼容

Hermes Agent兼容agentskills.io开放标准，技能可以跨Agent框架移植。

### 技能自动生成

Agent在完成复杂任务后自动生成Skill模板：
1. 识别可复用的任务模式
2. 提炼为流程化步骤
3. 在后续使用中根据结果优化

来源：[v0.2.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）
来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）

---

## MCP集成生态

### MCP客户端能力（v0.2.0+）
- stdio和HTTP两种传输协议
- 自动重连
- 资源/提示发现
- Sampling（服务器发起LLM请求）

### MCP服务器管理CLI（v0.4.0+）
- `hermes mcp`命令安装、配置、认证MCP服务器
- 完整OAuth 2.1 PKCE流程

### MCP服务器模式（v0.6.0+）
- 将Hermes暴露为MCP服务
- 兼容Claude Desktop、Cursor、VS Code等MCP客户端
- 支持stdio和Streamable HTTP传输

### ACP：客户端提供MCP服务器（v0.7.0+）
- IDE集成（VS Code、Zed、JetBrains）可注册自己的MCP服务器
- Hermes自动识别为Agent工具

### MCP OAuth 2.1 + 安全扫描（v0.8.0+）
- 标准兼容的OAuth认证
- OSV漏洞数据库自动扫描MCP扩展包

来源：[v0.2.0-v0.8.0 Release Notes](https://github.com/NousResearch/Hermes-Agent/releases)（一手）

---

## 竞品对比

| 特性 | Hermes Agent | OpenClaw | Claude Code | AutoGPT | Devika |
|------|-------------|----------|-------------|---------|--------|
| 开源 | MIT | MIT | 否 | MIT | MIT |
| 学习循环 | 内置 | 有限 | 否 | 否 | 否 |
| 消息平台 | 15+ | 5+ | CLI/IDE | CLI | CLI |
| 模型支持 | 200+ | 10+ | 1（Claude） | 多个 | 多个 |
| 终端后端 | 6种 | 2-3种 | 1种 | 1种 | 1种 |
| 记忆系统 | 持久化+插件 | 基础 | 无 | 有限 | 有限 |
| 插件系统 | 是 | 否 | MCP | 否 | 否 |
| MCP支持 | 客户端+服务器 | 有限 | 原生 | 否 | 否 |
| 技能系统 | 70+自动生成 | 手动 | Skills | 否 | 否 |
| 子Agent | 是 | 否 | 否 | 有限 | 否 |
| 定时任务 | 内置Cron | 否 | 否 | 否 | 否 |
| IDE集成 | ACP | 否 | 原生 | 否 | 否 |
| 更新频率 | 每2-3天 | 低 | 高 | 低 | 停滞 |
| OpenClaw迁移 | 内置 | — | — | — | — |

**Hermes Agent的核心生态优势**：
1. 最广泛的平台覆盖（15+消息平台）
2. 唯一内置学习循环的开源Agent
3. 最灵活的模型选择（200+模型，无锁定）
4. 最完整的MCP实现（客户端+服务器+OAuth）
5. 极快的迭代速度（27天7个版本，1000+PR）

来源：综合各项目GitHub仓库和官方文档对比分析

---

## 社区数据

| 平台 | 链接 | 说明 |
|------|------|------|
| GitHub | [NousResearch/hermes-agent](https://github.com/NousResearch/Hermes-Agent) | 主仓库 |
| Discord | 官方Discord社区 | 实时讨论和支持 |
| Skills Hub | 官方Skills Hub | 社区技能市场 |
| 文档 | [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs) | 完整文档 |

来源：[Hermes Agent GitHub README](https://github.com/NousResearch/Hermes-Agent)（一手）
