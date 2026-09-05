# Mac 专用 Penpot 设计工作区

本项目是服务多个业务项目的独立 Penpot 设计工作区，负责共用设计工具、组织业务设计资料、执行设计与审阅，以及交付设计成果。
共用工具及规则在 `penpot-kit/`；业务材料分开放在 `business-projects/<slug>/`。
本项目维护工作区内的工具、规则和设计材料，将业务项目规范作为设计输入。设计审批覆盖明确的设计对象、操作范围和提案版本；交付后的实施、发布与验收由接收项目按自身授权流程处理。

<!-- penpot-ai-kit:begin -->
# Penpot AI Kit — operating rules
This client uses the Penpot AI Kit at `penpot-kit/`, relative to this workspace root.

Before ANY Penpot design work:
1. Read penpot-kit/AGENTS.md and follow it (tokens-first; never one-shot; Suggest → Apply-with-review; honor the explicit approval gates and their recorded scope; keep the fill policy in penpot-kit/shared/modes-and-policies.md).
2. Your FIRST Penpot tool call each session is `high_level_overview` (no arguments).
3. Route the request via penpot-kit/skills/penpot-router/SKILL.md — choose exactly ONE skill or workflow, then open and follow that skill's SKILL.md.

- Skills:    penpot-kit/skills/<name>/SKILL.md
- Workflows: penpot-kit/workflows/<name>/
- Doctrine the skills rely on: penpot-kit/shared/ and penpot-kit/policies/ — consult it; never invent Penpot API calls (verify with `penpot_api_info`).

For Penpot design tasks only: when the request is underspecified, use the matching brief template in penpot-kit/prompts/ (design-brief, component-spec, migration-brief, audit-request). Fill known fields from the request, prior confirmed answers, and read-only discovery. Ask only for remaining information that materially affects the design objective, scope, or approval decision; continue independent read-only work while waiting. Keep every applicable explicit mutation-approval gate. To resume an interrupted multi-phase run, use penpot-kit/prompts/resume-continuation.md.
<!-- penpot-ai-kit:end -->

## 项目内路径与安装维护

- 首次从普通文件夹副本使用时，在 macOS 运行 `python3 tools/prepare.py` 恢复技能相对符号链接，再执行校验。此命令只替换已知链接占位文件，不修改 Kit。
- 项目级 Skills 在 `.agents/skills/`，使用相对符号链接指向 `penpot-kit/skills/`，只有这一份技能正文。
- Kit 文档中的 `shared/`、`policies/`、`skills/`、`workflows/`、`prompts/`、`templates/` 和 `scripts/install/` 均相对 `penpot-kit/`；单个技能的 `references/`、`scripts/` 相对该技能目录。跨文档链接按所在文档解析；有疑问先核实实际文件，勿猜路径。
- 安装维护依 `docs/maintenance.md`。保留本机定制，禁止自动安装、升级或卸载全局资源。Kit 原生命周期脚本已禁用，不能移除保护来运行它们。
- 日常工作规则从当前 `penpot-kit/` 加载；项目资料使用相对路径，不保存其他项目的历史指令、用户配置或凭据。
- 文件系统安装维护按已授权的维护范围执行；画布设计按 Kit 的 token、逐框、逐区块及高风险操作审批执行。

## Task scope and skill composition

- Keep the user's complete requested outcome as the parent task. Finishing a skill, demo, or handoff does not finish outstanding requested work.
- Choose one workflow to coordinate the task; load supporting skill guidance only for the subtask it actually governs. Loading design advice alone does not start an interview or concept-selection workflow.
- Check each approval gate's actual trigger. Preserve every applicable explicit approval; do not route around it. Reuse a recorded approval for the same object, scope, and proposal version, but do not infer approval of future phases from praise, silence, or elapsed time.
- An action request authorizes its stated scope, not unrelated edits or external actions. Read-only requests remain read-only. Continue independent authorized work when another part needs input, and report pending work without calling the whole task complete.
