# Local Agent Guidance

## Development Workflow

First select the task type and validation depth in
[Brendan's personal workflow](/Users/brendan/.agents/workflows/redo-development.md).
Investigations stay read-only. Data maintenance uses a short plan, dry run and
focused checks without architecture approval or a full app stack by default.
New product-development work defaults to
[RMR Engineer](/Users/brendan/.agents/skills/rmr-engineer/SKILL.md), including
automatic architecture review, scoped validation and one human release gate.
Instructions/configuration and other explicitly selected or already established
workflows retain their own paths. Do not require a separate RMR Engineer
invocation for each new product-development chat.

All Bazel, builds, types, lint, generation, dependency installation and
application tests run in Cloud, including quick checks and manage scripts.
Choose Cloud checks with `Runtime: none`, or Cloud runtime proof using only the
script, services or UI required by the acceptance checks. Use the repository's
`cloud-buddy` skill as the local workflow's remote executor and reuse its VM.
Preserve selected environments, stores and existing stacks. Local bounded,
read-only Waypoint queries through an existing approved client can supply
required database evidence; PGMask access alone does not prove performance.
Docs, skills and config that need only static checks can stay local.

Codex owns committed changes; validation helpers return evidence and patches.
Include the applicable personal rules and validation choice in Cloud briefs
because ignored instructions do not travel with Git. Use the Buddy push and
shared Cursor-agent helpers under the personal shared-branch rules. Do not use
`--no-verify` or fall back to local builds or `/validate`'s local Bazel launcher.

If Cloud Buddy is needed and absent, inspect the current skill from a fetched
`origin/main` with read-only Git. Preserve the active checkout and unrelated
work; do not switch branches or discard work to obtain the skill.

## New Worktrees and Checkouts

Before creating a new worktree or checkout, fetch `origin/main` and use that
freshly fetched revision as the starting base so it includes the latest changes
from `main`. Use a different base only when Brendan explicitly instructs it.
If fetching fails, report the blocker before proceeding with stale refs.
Preserve existing checkouts and uncommitted work.

## PR and MR Descriptions

- Keep descriptions concise: usually one or two short paragraphs explaining
  the problem and resulting behavior, followed by a brief validation note.
- Aim for roughly 100 words or fewer for straightforward changes. Add detail
  only when reviewers need it to understand a meaningful risk or tradeoff.
- Omit conversational history, file-by-file summaries, exhaustive test lists,
  and explanations of unchanged behavior. Include relevant ticket links and
  material validation limitations.
- Keep generated HTML walkthroughs (such as
  `output/<task>/walkthrough.html`) as local review artifacts. Never include
  them in commits or GitLab MR diffs.

## RPC Handlers

- Put each RPC handler in its own kebab-case module named after the endpoint.
  Register the lazy handler from that module directly. Keep a helper in a
  feature-local module only when more than one endpoint needs it.

## Function Names

- Name functions with a clear, active verb phrase in camelCase. Keep names
  concise, but descriptive enough to reveal intent without opening the body.
- Name helper functions for the operation they perform, not for a particular
  callsite or feature that happens to use them. For example, a helper that
  builds a Cockroach `PgClient` for a session should be named for creating or
  obtaining that connection, not for assignment capture.

## RPC Operations

- Prefer one RPC per independently invocable domain operation. Name it with an
  action and resource, give it only the inputs that operation needs, and return
  an operation-specific result. Use a command/discriminated union only when a
  single atomic transaction must accept heterogeneous operations.
- Design each RPC as a standalone tool: use canonical IDs, make the action
  explicit, and return enough state or identifiers for a caller—human or
  automated—to determine the next step without interpreting another endpoint's
  command vocabulary.
