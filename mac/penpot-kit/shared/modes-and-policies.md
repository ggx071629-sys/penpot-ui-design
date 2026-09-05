# Operating Modes & Policies

> The three modes every skill operates under, and the rule for what may happen without asking. `policies/modes.json` encodes the per-skill defaults; this file explains them.

Design decisions are often ambiguous, political, or product-level. An agent must never quietly make
irreversible or opinionated changes. Three modes govern every action.

## The three modes

| Mode | The agent... | Default for |
|------|--------------|-------------|
| **Suggest** | Proposes changes as a report/diff. Touches nothing on the canvas. | Audits, reviews, anything exploratory. |
| **Apply-with-review** | Performs the authorized phase, verifies it, then shows the result (`export_shape` + a summary) at its named approval checkpoint before continuing. Explicit pre-write approvals must already be satisfied. | The default for all generative/mutating skills. |
| **Auto-fix** | Applies a change without asking — **only** for changes in the explicitly-enumerated "safe set". | A narrow allowlist (below). |

**Global default: `Suggest → Apply-with-review`.** Auto-fix is opt-in per change type and scope, never per skill wholesale. The safe set establishes eligibility, not permission. An explicit request to perform that change type on an identified scope can supply the opt-in; an audit request or merely loading a skill cannot. Preserve any skill-specific requirement to approve a concrete proposal, and reuse an existing approval only while its object, scope, and proposal remain unchanged.

## The "safe set" (the only things Auto-fix may touch)
A change qualifies as safe only if it is **non-destructive, reversible, and unambiguous**:
- Renaming an unnamed / auto-named layer (`Rectangle 12` → semantic name).
- Replacing a raw value that is **exactly equal** to an existing token's resolved value with that token (a pure, loss-less swap).
- Sorting/ordering documentation pages or layer trees without changing geometry.
- Adding documentation/metadata (descriptions, plugin-data tags).

## Never Auto-fix (always require review)
- Anything that changes **geometry** (position, size, layout).
- Creating, deleting, or restructuring **variants** or **components**.
- `detach()` on a component instance.
- Creating a **new token** (propose it; let a human approve the name/value/tier).
- Deleting or renaming **shared** library assets.
- Anything where the matching token is a judgement call, not an exact equality.

## Mandatory user checkpoints
Use `policies/approval-checkpoints.md` to distinguish `verification` from `approval`. Internal
verification does not require a reply; every applicable named user-approval checkpoint still does.
An unclassified checkpoint that explicitly asks for approval remains an approval gate.
Rule: **"looks good" approves only the phase just shown — never a future phase.** Always name
the next phase explicitly. Showing the result does not create permission for the next phase.

New-token proposals must receive approval before creation; Apply-with-review does not postpone
that approval until after writing. The same holds for explicit pre-write gates on detach, deletion,
shared assets, and variant restructuring. In an authorized review phase, verification may include
targeted corrections that restore its agreed implementation; it does not authorize a new design
decision, add an item to the Auto-fix safe set, or bypass the phase's user-approval checkpoint.

## Justified explanations
On every applied change, the agent records *why*: which token/component/rule drove it, what
alternative was rejected, and any usability trade-off assumed. This is what makes the work auditable.

## Fill policy: structural vs. surface boards
Every Board is born with an opaque white fill (see `plugin-api-gotchas.md` #11). Leaving it there is a
bug, not a default. Classify **every** board you create or wrap:

- **Structural** — a layout-only container (screen sections, rows, stacks, variant containers,
  `button-group`, any wrapper produced by `clone()` / `createComponent` / `createVariantFromComponents`).
  It carries no colour of its own → **clear it: `board.fills = []`.** Transparent containers let the
  screen background show through and never defeat a child's border-radius.
- **Surface** — a board that is genuinely a painted surface: the **screen root** (one bg for the
  whole screen), a **card/sheet/panel**, or a **control** (button/input/chip). It carries colour →
  **bind a `color.bg.*` token** (`applyToken(tok, ["fill"])`), never a literal hex. Because it is
  bound by name, it flips correctly in dark mode.

Heuristic: if removing the fill would change nothing visible (it only ever sits behind other filled
shapes that cover it), it is structural — clear it. Exactly **one** board per nesting level should be
a surface; everything between surfaces is transparent.

## Token modes: `modes/light` + `modes/dark`, not `semantic` + `semantic-dark`
Dark mode is modelled as **two mutually-exclusive colour sets in a `modes/` group**, with the
mode-invariant semantics kept separate:

| Set | Holds | Active by default |
|-----|-------|-------------------|
| `primitives` | raw ramps/scales (mode-agnostic) | ✅ |
| `semantic` | **mode-invariant** semantics only — `spacing.*`, `radius.*`, `font.*` (reference primitives) | ✅ |
| `modes/light` | **colour** semantics for light — `color.bg.*`, `color.text.*`, `color.action.*` … (reference primitives) | ✅ |
| `modes/dark` | the **same colour names** with dark values (reference primitives) | ⛔ inactive |

Why this and not `semantic` + `semantic-dark`:
- **Symmetry** — light is an explicit set, not "the un-suffixed default". Less confusing.
- **Single responsibility** — `modes/*` holds *only* the colours that flip; `semantic` holds the
  spacing/radius/type that must *not* duplicate per mode. (The old `semantic-dark` only ever had the
  colours anyway — 8 of 15 — which is exactly the smell this fixes.)
- **Maps 1:1 to Penpot Themes** — a "Light"/"Dark" Theme just toggles `modes/light`↔`modes/dark`.

Bindings resolve **by token name** across whichever set is active, so a shape bound to
`color.bg.app` flips when the user activates `modes/dark`. The agent builds both sets, leaves
`modes/light` active, and hands the toggle to the user (`theme.addSet()` still does not persist via
the plugin — see `penpot-foundations/references/04-themes-modes.md`).
