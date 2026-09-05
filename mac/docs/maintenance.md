# 工作区维护与故障排查

首次使用请从[根目录 README](../README.md)开始。`penpot-kit/` 是当前工具集，`.agents/skills/` 通过相对符号链接引用技能正文；业务资料保存在 `business-projects/`。

## 本地校验

在项目根目录运行：

```sh
python3 tools/prepare.py
python3 tools/workspace.py verify
```

需要 Python 3.9+ 和 Node.js 22+，无需安装第三方 Python 包或 Node 依赖。成功输出 `passed: 8`、`total: 8`、空 `errors`，退出码为 0；任一检查失败退出码为 1，并在 `errors` 说明原因。

校验只检查当前项目和运行时版本，不读取个人客户端配置，不访问其他业务仓库，不连接 Penpot，不修改文件或生成报告。`kit_content` 和 `content_lock` 依赖 Node.js；运行时缺失时会报告未执行。

## 故障排查

| 现象 / 检查项 | 处理方法 |
|---|---|
| `python3` 命令不存在 | 在 macOS 安装 Python 3.9+ 并重新打开终端；Windows 请使用 Windows 专用版。 |
| `node_runtime` 失败 | 检查 `node --version`，确保 22+ 且客户端运行环境的 PATH 可找到它；安装后重新打开客户端。 |
| `workspace_files` / `business_template` 失败 | 按错误列出的相对路径恢复缺失文件或模板目录。 |
| `project_skill_links` 失败 | 检查是否漏了隐藏 `.agents/`，或解压把链接变成普通文本。单个链接如 `.agents/skills/penpot-router` 应指向 `../../penpot-kit/skills/penpot-router`。先运行 `python3 tools/prepare.py` 恢复已知占位文件；未知内容会拒绝覆盖，需人工核实。 |
| `skills.json` 损坏或 `kit_content` 失败 | 根据诊断修复清单、技能正文或依赖关系；必要时重新获取完整工具集。不要用更新锁文件掩盖缺失或损坏。 |
| `content_lock` 失败 | 先确认内容变化是预期且已获准；意外变化应恢复，获准修改才按下节重新生成锁文件。 |
| `lifecycle_guards` 失败 | 恢复安装脚本中的保护入口；不要通过取消校验或运行安装器解决。 |
| Codex 找不到技能 | 从项目根目录打开任务，先检查技能链接，再重新打开客户端；核对 [Skills 官方说明](https://learn.chatgpt.com/docs/build-skills)。 |
| 看不到 Penpot MCP 工具 | 检查客户端中的 MCP 服务是否启用，配置后重启连接；按 [MCP 官方说明](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)核对配置格式。 |
| `No plugin instance connected` | 在目标 Penpot 文件重新连接 MCP，并保持文件及插件连接；按 [Penpot 官方指南](https://help.penpot.app/mcp/)检查模式和连接步骤。 |
| 当前文件或页面不对 | 切换到目标页面并重新只读确认，确认对象前不写入画布。 |

终端校验通过但客户端仍找不到 Node.js 时，两者可能使用不同的 PATH。不要把他人的个人路径直接复制到项目规则中。

## 修改工具集

只在用户授权范围内修改，保留设计规则和明确审批要求。禁止自动安装、升级、卸载全局资源，禁止移除生命周期保护后运行安装脚本。

获准修改 Kit 后，依次执行；前一步失败时先修复：

```sh
node penpot-kit/scripts/dev/validate-kit.mjs
node penpot-kit/scripts/dev/update-lock.mjs
python3 tools/prepare.py
python3 tools/workspace.py verify
```

锁文件校验当前内容，不代表设计通过审阅。业务项目的实施、发布与验收按各自授权流程处理。

## 转交前检查

按 README 的分享范围制作副本，排除业务内容、Git 历史、个人配置和凭据，保留相对符号链接。在新目录运行 `verify`，再由接收者完成真实客户端的技能发现及 Penpot 只读连接确认。

Kit 内多客户端安装文档属于技术参考；当前工作区的使用入口和维护规则以根目录 README 及本文为准，不运行禁用的生命周期脚本。
