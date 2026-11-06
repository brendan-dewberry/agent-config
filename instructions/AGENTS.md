## Writing style

At the start of each chat, read the
[unslop skill](/Users/brendan/.agents/skills/unslop/SKILL.md) and apply it to all
prose you write, including progress updates, final replies, walkthroughs,
documents, merge request descriptions, and commit messages. Apply its editing
rules before delivering the text.

Preserve facts, technical detail, meaningful uncertainty, exact quotations, and
code identifiers. Follow the user's requested tone and format. Never sacrifice
clarity merely to shorten the text.

## Task scope

- Keep changes tied to the requested outcome and its acceptance requirements.
  Trace and reuse existing behavior before adding new code or infrastructure.
- Preserve the agreed owner of a workflow. An agent workflow change belongs in
  its instructions, skills and existing tools unless a concrete capability gap
  requires application or platform code. Do not duplicate that workflow in a
  new controller, scheduler or state machine as an implementation convenience.
- Necessary supporting changes must have a direct, explainable connection to
  the task. Present broader behavior, ownership or architecture changes
  separately and get agreement before implementing them. Adjacent cleanup,
  generic hardening and future capabilities are separate work.
- When the approach or scope narrows, remove the superseded code, dependencies,
  tests and documentation. Do not retain them just because they were already
  written. Review the final diff against the current request before delivery.

## Personal domain documentation

Before investigating, planning, or implementing in a Git repository, check
`<repo-root>/.agent-notes/domain-modeling/` for personal domain documentation.
Read these paths explicitly because Git-aware searches may skip ignored files.
If present, read `GLOSSARY-MAP.md` and the glossaries it identifies as relevant,
or `GLOSSARY.md` for a single context, plus decision records relevant to the task
under `docs/adr/` or the mapped context directories. If absent, proceed silently.

Use the glossary's terminology and consider recorded decisions. Verify factual
claims against current code, and surface conflicts or stale notes rather than
treating them as current behavior. Keep these notes local and ignored, outside
project commits and merge requests. When using Matt Pocock's skills, resolve
their glossary and ADR references to this personal documentation root.

## Redo Development Workflow

For Redo development tasks in either local checkout, read and follow
[Brendan's agentic development workflow](/Users/brendan/.agents/workflows/redo-development.md).
Use the active checkout's `.agents/skills/architecture-review/SKILL.md` for
planning and implementation walkthroughs. Honor approvals and environment
choices already given in the conversation. Include the applicable workflow in
cloud handoff briefs because the Redo repository does not contain this personal
workflow.

## Merge Request Links

- When sharing Redo merge requests with Brendan, use their LGTM links instead
  of GitLab links in replies, walkthroughs, and review artifacts.
- Resolve the actual LGTM URL for the MR; do not invent a URL pattern.

## Git Checkout Safety

- Inspect the checkout's branch and status before working, and preserve
  existing changes.
- Do not stash, reset, clean, or switch away from uncommitted changes without
  my explicit direction.

## RPC File Organization

- Keep one RPC handler per server handler file, with the file named for that
  RPC. Do not group several RPC handlers in a domain-themed handler module.
- Keep each RPC schema definition in its own schema file as well. Shared
  helpers belong in a separate service or utility module and may be reused by
  the individual handlers.

## Function Organization

- Keep each function focused on one responsibility. A workflow function should
  read as a short sequence of named domain steps.
- Extract cohesive decisions or operations into helpers with names that explain
  their purpose; avoid both long mixed-responsibility functions and tiny
  pass-through wrappers.
- Preserve important boundaries such as transactions: keep related reads and
  writes explicit, and pass the transaction into helpers that participate in
  it.
- Prefer early returns for terminal cases and group related inputs in a named
  object when a helper needs several values.

## Repository Modules

- Keep database writes in repository modules dedicated to the table they own.
  Reuse an existing repository before adding one. Keep business rules and
  multi-table workflow coordination in services, passing the same transaction
  into participating repository methods.
- Give repository methods concise action names. Let the module identify the
  entity instead of repeating it in every method: `createSession`, `getSession`,
  and `updateReceivingSource`, rather than `createItemProcessingSession`.
- Import repositories directly as module namespaces with descriptive PascalCase
  names, for example:

  ```ts
  import * as ItemProcessingRepo from "./item-processing-repo";

  await ItemProcessingRepo.createSession(input, txn);
  ```

- Export individual functions from repository modules. Prefer static member
  calls (`ItemProcessingRepo.createSession`) over dynamically indexing, spreading,
  or passing the entire namespace, so bundlers can identify used exports.

## Redo Agents API

When investigating or managing agents at `agents.redo.builders`, load the
`redo-agents-api` skill. Use the documented HTTP API and the local
`REDO_AGENTS_API_KEY` or `~/.config/redo-agents/api-key` before reaching for the
browser. A missing MCP connector does not mean the HTTP API is unavailable.
Verify access with `GET /v2/me`; never print or log the key. Use the browser
only for browser-only routes or when the key lacks the required access.
