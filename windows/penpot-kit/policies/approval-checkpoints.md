# Approval checkpoints

Shared checkpoint rules across all skills/workflows.

## The core rule
**"Looks good" approves only the phase just shown — never a future phase.** Always name the next phase
explicitly before proceeding.

## Checkpoint types
- **Verification:** inspect structure, tokens, or screenshots; report the result and continue within the already authorized phase. A visible progress artifact is not automatically a request for permission.
- **Approval:** name the concrete proposal or phase result, target, scope, and next action; wait for explicit approval unless that exact unchanged proposal has already been approved. A recap, silence, or approval of an earlier phase cannot approve a future one.
- Existing hard gates in the matrix below remain approval gates. Only explicitly informational checkpoints and the scoped safe-rename exceptions are verification-only.
- Targeted self-correction may restore the current authorized phase's agreed implementation before its result is shown. It may not introduce new design decisions or skip new-token, detach, deletion, shared-asset, or variant-restructuring approvals. Keep per-frame and per-section approvals.

## At every approval checkpoint, show
1. **Evidence** — an `export_shape` (`'selection'` or `'page'`) of what changed, and/or a structured
   read (`shapeStructure` / `tokenOverview`).
2. **Summary** — what was created/changed, tokens used, anything proposed, assumptions.
3. **The ask** — a specific question ("Approve these tokens? Next I'll build components.").

## Checkpoint matrix (typical)
| Skill | Hard checkpoints (require approval) |
|-------|--------------------------------------|
| penpot-foundations | approve concrete primitive, semantic, and theme proposals before writing each; approve the binding proposal before applying to shapes unless its scoped exact-swap opt-in already applies; verify resulting values without reapproving the same proposal |
| penpot-component-factory | after axis matrix, after base, after variants, before combining |
| penpot-build-screen | after direction, after frame, after each section, after assemble |
| penpot-build-from-code | after discovery, after each section |
| penpot-migrate | after scope/mapping, after IR, after tokens, after components, per screen |
| penpot-audit-* | after the report (before any fix) |
| penpot-rename-layers | safe-set renames require a scoped opt-in; with it and a clear scope, inventory/result are informational; approve concrete meaningful-name and ambiguous rows before writing |

## Destructive / irreversible actions
Always require explicit approval, regardless of mode: `detach()`, deleting/renaming shared assets,
deleting shapes, restructuring variants. Record the rationale in the run report.
