# Penpot 独立设计工作区

一套面向 Codex 本地任务的可复用设计工作区：你提供业务想法或方案，助手整理需求，在 Penpot 中分步设计、审阅并交付可编辑成果。

[Penpot AI Kit](https://github.com/penpot/penpot-ai-kit) 是位于 Penpot 官方 GitHub 组织下的开源工具包，提供 AI 设计技能、工作流和操作规则。本项目在其基础上增加 Mac / Windows 工作区适配、业务资料模板和本地维护工具，作为独立定制版本维护。使用本工作区无需运行 Kit 安装器。

## 选择平台版本

本仓库提供 `windows/` 和 `mac/` 两个独立项目，两者不依赖彼此或父目录中的工具文件。建议将所选目录完整复制到仓库外的独立位置，再在 Codex 中打开。

| 项目 | 适用环境 | 技能入口与维护 | 使用说明 |
|---|---|---|---|
| `windows/` | Windows | 普通技能目录；显式 UTF-8 编码和 LF 换行，无需管理员权限创建符号链接。维护 Kit 后同步技能副本。 | [Windows README](windows/README.md) |
| `mac/` | macOS | 保留相对符号链接；从文件夹副本首次使用时运行初始化命令恢复链接。 | [Mac README](mac/README.md) |

使用仓库里的 `mac/` 文件夹副本时，先进入该副本目录，运行 `python3 tools/prepare.py` 恢复链接。初始化只替换已知占位文件；已有正确链接保持不变，未知内容会拒绝覆盖。

请在 `mac/` 或 `windows/` 中开始设计任务；平台目录各自包含完整的技能入口。

根目录仅保留 README 总入口、两套平台工程及 Git 配置等隐藏项。以下使用流程中的“项目根目录”和命令路径，均指所选平台目录或其独立副本的根目录。业务资料分别存入对应项目的 `business-projects/`；两个版本的 Kit 后续维护不会自动相互同步。

## 使用前准备

| 要求 | 用途 |
|---|---|
| 可访问本地文件、使用 Skills 和 MCP 的 Codex 客户端 | 读取项目规则、执行设计任务 |
| Python 3.9+，终端中能运行 `python3`（Windows 可用 `python`） | 工作区校验，无第三方 Python 依赖 |
| Node.js 22+，终端中能运行 `node` | Kit 校验，无需为此运行 `npm install` |
| Penpot 账号及目标文件访问权限 | 打开设计文件并启用 MCP |
| 保留隐藏目录及 `.gitattributes` 的完整项目副本 | Windows 保留普通技能目录；Mac 保留或初始化相对符号链接 |

Python 和 Node.js 是本工作区维护工具的要求；远程 Penpot MCP 无需在本机启动 MCP 服务。

## 首次使用

### 1. 打开并检查工作区

将所选平台目录复制到独立位置，保留 `.agents/` 等隐藏目录及 `.gitattributes`。先在终端进入该目录完成以下初始化和校验，再在 Codex 中打开它；不要只打开 `penpot-kit/`。

Windows 在所选项目根目录的终端运行：

```powershell
python --version
node --version
python tools/workspace.py verify
```

Mac 在所选项目根目录的终端运行：

```sh
python3 --version
node --version
python3 tools/prepare.py
python3 tools/workspace.py verify
```

Windows 版校验脚本已显式使用 UTF-8，无需额外添加 `-X utf8`。Mac 版首次处理文本占位文件时会显示 `Restored 12 relative skill links.`，再次运行显示 `Restored 0 relative skill links.`。副本已带正确链接时，首次运行也可显示 0。

如果直接在 Git 仓库内初始化 `mac/`，Git 会将 12 个入口显示为文件类型变化（`T`）：文本占位文件变成了符号链接，这是初始化的预期结果。在独立副本中初始化可保持原仓库不变。

应得到 `passed: 8`、`total: 8`、空的 `errors`，退出码为 0。失败时按 `errors` 排查，见 [Windows 维护说明](windows/docs/maintenance.md)或 [Mac 维护说明](mac/docs/maintenance.md)。

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

在已初始化的平台副本中打开新任务，发送：

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

不需要提前填满模板。设计建议与已确认内容分开，审批与交付记录随实际进度补充。设计按页面和区块逐步完成，优先复用组件及样式，并在适用节点请你审阅。业务项目负责后续开发、发布与验收。完整任务启动约定见 [Mac 启动说明](mac/docs/start-task.md)或 [Windows 启动说明](windows/docs/start-task.md)。

## 项目结构

根目录组织如下：

```text
README.md        使用总入口
mac/             Mac 独立工程
windows/         Windows 独立工程
.*               Git 配置等隐藏文件及目录
```

`windows/` 和 `mac/` 各自包含下面的完整结构：

| 路径 | 作用 |
|---|---|
| `AGENTS.md` | AI 的工作范围、规则和审批边界 |
| `.agents/skills/` | Codex 技能发现入口 |
| `penpot-kit/` | 技能、工作流、规则、脚本及技术参考 |
| `business-projects/` | 空模板和各业务项目的设计资料 |
| `docs/` | 任务启动、维护和故障排查说明 |
| `tools/workspace.py` | 只读环境及结构校验 |

Windows 另有 `tools/sync-skills.py`，用于从 `penpot-kit/skills/` 更新生成的技能副本；Mac 另有 `tools/prepare.py`，用于恢复相对技能链接。请只维护各版本的 Kit 源文件，Windows 技能副本中的直接修改会在同步时被覆盖。

## 分享此工作区

分享所选平台项目时，保留 `AGENTS.md`、`README.md`、`.gitignore`、`.gitattributes`、`.agents/`、`penpot-kit/`、`docs/`、`tools/`，以及 `business-projects/README.md` 和 `_template/`。Windows 使用普通目录；Mac 打包时保留符号链接，或让接收者运行初始化命令恢复链接。

公共模板不要包含实际业务项目目录、`.git/`、`.local/`、个人配置、凭据、缓存或系统杂项。`.gitignore` 只影响 Git，不会替普通文件夹压缩自动排除这些内容。接收者需要自行配置账号和 MCP。

## 已验证范围与限制

- **已验证环境**：macOS arm64（Python 3.14.7、Node.js 24.19.0、Codex CLI 0.153.1）；Windows x64（Python 3.11.9、Node.js 24.18.0）。
- **Mac 版**：工作区校验 8/8 通过；初始化可重复运行并保护未知文件；独立副本支持中文和空格路径，12 个项目技能均可被 Codex 正确发现。
- **Windows 版**：本地工具与独立副本校验通过，支持技能副本内容漂移、文件缺失检测及同步恢复。
- **使用限制**：根目录不作为设计工作区；使用对应平台目录或其独立副本。平台目录中的技能入口分别维护。Linux 不在这两个专用版本的适配范围内。
- **连接要求**：本地校验仅覆盖工具和文件结构；使用前需自行配置 Penpot MCP，并确认目标文件连接正常。

## 来源与许可

上游工具包：[Penpot AI Kit — penpot/penpot-ai-kit](https://github.com/penpot/penpot-ai-kit)，仓库归属 Penpot 官方 GitHub 组织。

`mac/penpot-kit/` 和 `windows/penpot-kit/` 为分别维护的定制副本，所附 `package.json` 标注版本 0.3.0、许可 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。本地版本与上游分别维护，不能仅凭上游仓库的状态判断本地功能或版本。分享时保留工具集已有的来源与许可说明。

本工作区的定制包括项目级技能入口、业务资料模板、操作说明、校验工具，以及设计审批和生命周期保护调整。业务资料及设计成果不因放入此目录而自动采用工具集许可；对外提供时需分别确认授权范围。
