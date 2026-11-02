---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Generated documentation is personal and must stay out of project commits and
merge requests. Use `<repo-root>/.agent-notes/domain-modeling/` as the
documentation root. All `GLOSSARY.md`, `GLOSSARY-MAP.md`, and `docs/adr/` paths
below and in the bundled formats are relative to this documentation root.

Before writing any documentation:

1. Resolve the active repository root with `git rev-parse --show-toplevel`.
2. Check `git ls-files -- .agent-notes` from that root. If any generated notes
   are already tracked, stop and explain that ignore rules cannot untrack them.
3. Resolve the local exclude file with `git rev-parse --git-path info/exclude`
   from that root. Append `/.agent-notes/` if it is not already present,
   preserving the existing contents. Create its parent directory if needed.
   This is a local Git setting; keep the project's tracked `.gitignore` intact.
4. Verify each proposed output is ignored with `git check-ignore` before writing.
   Keep every generated output inside the documentation root.

Read existing project glossaries and ADRs as references when relevant. Keep
personal additions in this local documentation root rather than editing tracked
team documentation. Never stage, commit, publish, or force-add generated notes.
Creating team documentation requires the user's explicit direction.

Outside a Git repository, use `.agent-notes/domain-modeling/` under the working
directory and explain that no Git exclusion can be configured there.

Most projects have a single context:

```
.agent-notes/domain-modeling/
├── GLOSSARY.md
└── docs/
    └── adr/
        ├── 0001-event-sourced-orders.md
        └── 0002-postgres-for-write-model.md
```

If a `GLOSSARY-MAP.md` exists in the documentation root, the project has
multiple contexts. The map points to where each one lives inside that root:

```
.agent-notes/domain-modeling/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
└── contexts/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                 ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
