# Mac 专用 Penpot 设计工作区

一套面向 Codex 本地任务的可复用设计工作区：你提供业务想法或方案，助手整理需求，在 Penpot 中分步设计、审阅并交付可编辑成果。

本目录可独立复制和使用，不依赖旁边的 `windows/` 或父目录文件。保留 Mac 的相对符号链接方案和 LF 换行规则。

本项目是基于第三方 Penpot AI Kit 定制的工作区，不是 Penpot 官方产品，也不是一键安装插件。无需运行 Kit 安装器。

## 使用前准备

| 要求 | 用途 |
|---|---|
| 可访问本地文件、使用 Skills 和 MCP 的 Codex 客户端 | 读取项目规则、执行设计任务 |
| Python 3.9+，终端中能运行 `python3` | 工作区校验，无第三方 Python 依赖 |
| Node.js 22+，终端中能运行 `node` | Kit 校验，无需为此运行 `npm install` |
| Penpot 账号及目标文件访问权限 | 打开设计文件并启用 MCP |
| 保留隐藏目录和符号链接的完整项目副本 | 使 `.agents/skills/` 指向 `penpot-kit/skills/` |

Python 和 Node.js 是本工作区维护工具的要求；远程 Penpot MCP 无需在本机启动 MCP 服务。

## 首次使用

### 1. 打开并检查工作区

将整个项目放在你选择的位置，在 Codex 中打开根目录；不要只打开 `penpot-kit/`。保留 `.agents/` 等隐藏目录及 `.gitattributes`。若来自 Windows 文件夹副本，技能入口暂为链接占位文件；先在 macOS 运行下面的初始化命令恢复链接。保留链接的压缩包解压后也可运行，已有正确链接会保持不变。

在项目根目录的终端运行：

```sh
python3 --version
node --version
python3 tools/prepare.py
python3 tools/workspace.py verify
```

初始化完成后，在 Codex 中重新打开此目录，让客户端发现技能。`prepare.py` 仅支持 macOS，不需要运行 Kit 安装器。

应得到 `passed: 8`、`total: 8`、空的 `errors`，退出码为 0。失败时按 `errors` 排查，见[维护与故障排查](docs/maintenance.md)。

Codex 从 `.agents/skills/` 发现项目技能，并支持符号链接；本工作区提供 12 个 `penpot-` 技能。新任务中应能找到 `penpot-router`；没有出现时重新打开客户端并检查目录。参见 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills)。

### 2. 连接 Penpot

首次使用建议采用远程连接：

1. 在 Penpot 的 **Your account → Integrations → MCP Server** 启用 MCP，生成密钥并复制服务 URL。
2. 在 Codex 客户端的 MCP 设置中添加名为 `penpot` 的 **Streamable HTTP** 服务，粘贴该 URL，保存并重启连接。
3. 打开目标 Penpot 文件，通过 **File → MCP Server → Connect** 连接当前文件，并保持连接。

Penpot 的服务 URL 包含个人凭据，由接收者自行配置；不要放入业务方案、共享文件或本仓库。连接流程以 [Penpot 官方 MCP 指南](https://help.penpot.app/mcp/)为准。

若客户端没有图形配置入口，可以在用户级 `~/.codex/config.toml` 中合并以下配置，保留已有的其他设置；已有同名服务时编辑原表，不要重复添加：

```toml
[mcp_servers.penpot]
url = "在本机替换为 Penpot 提供的完整服务 URL"
```

该示例是占位符，不是可直接连接的地址。本工作区不附带个人配置，也不要求将凭据保存到项目级配置。配置格式见 [OpenAI MCP 文档](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)。自托管或本地 MCP 请按 [Penpot 官方指南的本地模式说明](https://help.penpot.app/mcp/#local-mcp-server)单独配置。

### 3. 做一次只读连接确认

在本项目新建任务，发送：

```text
请读取项目 AGENTS.md 和 penpot-kit/AGENTS.md，按 penpot-router 检查连接。
第一条 Penpot 工具调用使用无参数 high_level_overview。
只读确认当前文件、页面和现有组件，不修改画布，不输出连接凭据。
```

确认返回的是你要操作的文件和页面后，再开始设计。文件校验通过只表示工具完整，不表示 MCP 已连接。

## 开始第一个设计任务

你只需要提供项目名称、业务说明和本次设计目标。已有文档可以给出文件路径；风格、截图和 Penpot 链接有则补充。

```text
项目：我的业务项目
业务说明：给谁使用、解决什么问题、用户大致怎么操作。
本次目标：设计哪些页面、流程或组件。
已有资料：文档路径、参考图片或链接（可选）。
设计要求：设备、语言、风格及必须遵守的约束（可选）。

请先整理项目资料并提出设计方案，明确待确认的问题。
```

助手复制 `business-projects/_template/` 建立项目目录：

| 目录 | 内容 |
|---|---|
| `briefs/` | 业务需求、操作流程和本次范围 |
| `design-specs/` | 已明确的视觉、组件和交互规范 |
| `reviews/` | 实际审阅意见及对应对象、范围、版本的批准 |
| `deliverables/` | 设计成果、导出图和 Penpot 链接 |
| `handoffs/` | 实施说明及未解决事项 |

不需要提前填满模板。设计建议与已确认内容分开，审批与交付记录随实际进度补充。设计按页面和区块逐步完成，优先复用组件及样式，并在适用节点请你审阅。业务项目负责后续开发、发布与验收。完整任务启动约定见[启动说明](docs/start-task.md)。

## 项目结构

| 路径 | 作用 |
|---|---|
| `AGENTS.md` | AI 的工作范围、规则和审批边界 |
| `.agents/skills/` | Codex 技能发现入口 |
| `penpot-kit/` | 技能、工作流、规则、脚本及技术参考 |
| `business-projects/` | 空模板和各业务项目的设计资料 |
| `docs/` | 任务启动、维护和故障排查说明 |
| `tools/workspace.py` | 只读环境及结构校验 |
| `tools/prepare.py` | 在 macOS 恢复相对技能符号链接 |

## 分享此工作区

分享项目文件时，保留 `AGENTS.md`、`README.md`、`.gitignore`、`.gitattributes`、`.agents/`、`penpot-kit/`、`docs/`、`tools/`，以及 `business-projects/README.md` 和 `_template/`。打包工具需要保留隐藏文件与符号链接。

公共模板不要包含实际业务项目目录、`.git/`、`.local/`、个人配置、凭据、缓存或系统杂项。`.gitignore` 只影响 Git，不会替普通文件夹压缩自动排除这些内容。接收者需要自行配置账号和 MCP。

## 已验证范围与限制

- 原工作区已验证环境：macOS arm64，Python 3.14.7，Node.js 24.19.0。
- 原工作区已完成同机干净目录副本校验：保留相对技能链接，不包含 `.git/`、用户配置或业务数据，并从含空格的新路径运行检查。
- 原工作区已验证常见失败提示：缺少 Node.js、技能链接损坏、清单损坏、锁文件不匹配、生命周期保护缺失。
- **平台范围**：Windows 请使用对应的专用版。
- **连接要求**：本地校验仅覆盖工具和文件结构；使用前需自行配置 Penpot MCP，并确认目标文件连接正常。

## 来源与许可

`penpot-kit/` 基于 [elhombretecla/penpot-ai-kit](https://github.com/elhombretecla/penpot-ai-kit)，所附 `package.json` 标注版本 0.3.0、许可 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。保留工具集的来源与许可说明。

本工作区的定制包括项目级技能入口、业务资料模板、操作说明、校验工具，以及设计审批和生命周期保护调整。业务资料及设计成果不因放入此目录而自动采用工具集许可；对外提供时需分别确认授权范围。
