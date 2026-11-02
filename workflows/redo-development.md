# Brendan's agentic development workflow

Personal workflow, agreed October 3 and updated November 2, 2026.
This canonical document is versioned in Brendan's private `agent-config`
repository and applies to both Redo checkouts. It is installed at
`$HOME/.agents/workflows/redo-development.md`. The previous Redo-local path is
an ignored symlink to this file.

Resolve repository-relative paths below from the active Redo checkout.

## Default workflow and precedence

Use the active task worktree's repository-managed
`cloud-buddy` skill at `.agents/skills/cloud-buddy/SKILL.md` for local
implementation paired with persistent Cursor Cloud validation. Read its current
skill, templates, push helper, and shared Cursor-agent runbook as needed. Start
the buddy when product code needs to be built, tested, or run; skip cloud setup
for docs, skills, and config-only changes. This replaces the earlier
`cloud-delegate` default and its orchestration, overlay, and Land-stage
mechanics. Keep the repository-managed skills intact; personal preferences
belong here and in local agent instructions.

The skill is already merged into main. If an older checkout lacks it, fetch
only the necessary main ref and inspect it with read-only Git. Create or reuse
a task worktree with the skill available at a recorded source revision. Do not
switch or update another owner's checkout, discard changes, or copy a stale
personal skill over the repository-managed one. An existing task's chosen base
and environment still apply; resolve dependencies before changing them.

Codex owns investigation, planning, implementation, orchestration, and review.
Cursor proves behavior and runs all builds, lint, type checks, generation,
tests, and services. Locally, use source edits, Git, static review, and the
skill's lightweight shell/API helpers. No local Bazel, Scurry, dependency
installation, lint, type checks, tests, or services unless Brendan explicitly
chooses an exception. Write meaningful regression coverage locally and run it
in the cloud.

## Personal rules for cloud briefs

Include these already-authorized preferences directly in the cloud-buddy brief
and append the shared Cursor-agent runbook as the skill instructs. Git does not
carry ignored files or the local conversation into worktrees or cloud agents
automatically. Do not depend on cloud-delegate's overlay or brief generator.

- Create the standalone HTML architecture plan and get Brendan's approval
  before implementing. Update that same walkthrough for implementation review.
  Existing approvals count; do not request them again for unchanged scope.
- Codex is the only code owner. Cursor reports failures and returns generated,
  formatting, or service-unblock fixes as patches for local review and commit.
  It does not commit or push application changes, even mechanical fixes, or
  open MRs. Temporary diagnostic edits must follow the buddy's brief.
- Temporary seeding, instrumentation, or generated changes must be disclosed.
  Evidence from a modified cloud tree is provisional until Codex commits the
  needed changes and Cursor validates the resulting clean candidate SHA.
- Honor the runtime and Dev Store already selected. If the selected store
  cannot be restored or accessed, mark dependent checks blocked; do not quietly
  substitute seeded data and call the original acceptance criterion passed.
- Provide a working demonstration for hands-on approval and review the final
  diff and affected callers. Plan approval, behavior approval, and "done" do
  not authorize heavy CI gates, merge, deployment, or production writes.
- Return screenshots or a short demo recording for user-visible changes, with
  the tested SHA, runtime, fixtures, and steps. Codex inspects the evidence and
  attaches it to the MR as described below.
- Keep MR descriptions concise and preserve unrelated checkout work. Do not
  spawn helper agents unless the user or an applicable instruction requests it.

## Delivery flow

1. **Investigate and plan.** Read current source, relevant docs, existing reuse,
   and selected validation playbooks. Establish intended behavior, scope,
   meaningful failure cases, and exact live proof. Produce the HTML plan and
   obtain approval before implementation.
2. **Implement locally.** Use one task branch/worktree and one code owner.
   Record the path, base SHA, branch, and owner. Write code and regression
   coverage, review the complete diff, and commit only intended changes.
3. **Start the buddy, push, and open a draft MR.** Start the buddy as soon as
   the product-code scope is known, while local work continues. Use the
   cloud-buddy brief template and shared Cursor-agent launch/watch helpers.
   Name the runtime, affected packages, expected behavior, and standing checks.
   Use `cloud-buddy/scripts/push.sh` subject to the shared-branch rules below,
   then create the draft immediately. Do not enable heavy CI.
4. **Iterate with Cursor.** Reuse the same buddy and runtime. After every push,
   have it fetch the exact candidate SHA and run the standing checks. Send
   additional questions through the shared followup helper and re-arm the
   watcher. Prove changed paths live and independently inspect the returned
   evidence. Apply suggested patches locally and push completed batches.
5. **Approve behavior and review implementation.** Provide verified links and
   test steps for Brendan. Attach validation evidence directly to the MR.
   Update the same HTML walkthrough with actual code, deviations, evidence,
   and gaps. Fix findings and revalidate affected paths.
6. **Complete final cloud checks when Brendan says done.** Use the same buddy
   for any remaining touched-package type checks, lint, generation, regression
   proof, and required tests. Cursor returns patches under the personal
   code-owner rule; Codex reviews, commits, and sends the resulting SHA back for
   checks. Every required check must pass on the final candidate.
7. **Finish deliberately.** Human approval is still required for ready state,
   `ready-for-ci`, starting a pipeline, merge/auto-merge, and deployment. Verify
   final evidence before requesting those actions. Shared skill/playbook changes
   need their own authorized MR; memory-folder updates need an explicit request.

Run the buddy's standing checks on each pushed candidate, including relevant
builds, lint, types, regression coverage, and live proof. Keep checks scoped to
what changed and verify that filtered test runs actually ran the intended
tests. No local checks are implied by the skill's allowance for quick checks;
the personal cloud-only preference above still applies.

## Worktrees, pushes, and setup

Worktrees are for source editing; do not initialize local runtime dependencies,
Bazel output bases, or build caches. Preserve existing work and configuration.
Make the private workflow readable in each task's local instructions without
replacing its other overrides. Remove only safely saved, clean worktrees with
cleanup direction; never delete dirty trees or caches automatically.

Use cloud-buddy's push helper and hook-specific switches instead of
`git push --no-verify`. Keep hooks enabled globally. Preserve the personal
merge-only, no-force-push rule while a branch is shared: fetch and incorporate
remote commits first. The buddy push helper currently uses
`--force-with-lease`; on a shared branch, use a normal push with the same
hook-specific switches, then send the resulting SHA through the shared
followup helper to request the standing checks.

Follow cloud-buddy's credential/setup rules. Credentials never appear in chat,
artifacts, or commits. A setup failure blocks dispatch, not independent
planning or local implementation. Do not fall back to local builds.

## Evidence and correction loop

Follow cloud-buddy's report and artifact formats: per-round `report.md`,
`report.json`, `updates.md`, and evidence retrieved with the shared artifacts
helper. Retrieve commands, logs, screenshots/video, and ground-truth data
appropriate to the feature.
A terminal agent status or a report alone is not a pass. Check expected versus
actual behavior, required items, tested SHA, and unresolved blockers. Mock UI
proof cannot establish backend persistence or correctness.

Reuse the same Cursor buddy/runtime across iterations and final checks. Require
proof for the current SHA; evidence retained from an older SHA remains labeled
with that revision. Changes affecting accepted behavior return to hands-on
acceptance. Keep a small task record of approvals, agent/run IDs, paths, branch,
MR, tested/source SHAs, preview availability, status, and next action.

Do not improvise validation prerequisites or fabricate a pass. Cloud failures
must include reproducible entry points, expected/actual results, logs, and
file/line evidence so Codex can correct the code locally.

## MR validation evidence

Before handing off an MR for review, put the validation results and evidence
on the MR itself. For user-visible changes, upload inspected screenshots or a
short demo recording and embed them in the description or a clearly linked MR
comment. Use before/after captures with the same input when they help explain
the change. Label mock screenshots as mocks. Evidence kept only in chat, local
files, or cloud-agent artifacts is not a completed review handoff.

Keep the description concise. Include the tested SHA, runtime, relevant
fixtures, commands and results, expected versus observed behavior, and remaining
gaps. Put longer evidence in a linked comment. Label older evidence with its
actual revision and explain any reuse; never imply it was rerun on the current
head. Verify that the saved MR renders the attachments and links correctly.

For a hands-on demo, include verified access instructions and reproduction
steps without credentials. Record when access was last verified. Keep durable
screenshots or a recording on the MR even when a live demo is available, and
label expired or unverified access clearly. Keep the personal HTML walkthrough
local unless Brendan asks to publish it. Posting evidence does not authorize
CI gates, ready state, merge, or deployment.

## Architecture walkthrough

Use the **repository-managed** skill at
`.agents/skills/architecture-review/SKILL.md`
in the active checkout. Read its current instructions and required references
for both plan and implementation review. It supersedes the earlier
`change-walkthrough` skill and personal copies for this workflow. Do not switch
branches merely to generate a document; disclose the source revision reviewed.

Maintain one self-contained HTML file per change, normally
`output/<change-slug>/walkthrough.html`, and update it in place. Default to the
skill's light mode, Redo orange, restrained styling, inline assets, and offline
operation unless Brendan requests another style.

Keep the explanation focused and one step above code:

- Start with the problem, intended behavior, and the central domain rule.
- Show before and after using the same concrete input. Use entity relationship
  diagrams for data models, sequence diagrams for interactions, or another
  visual that makes the change easier to understand.
- Explain ownership, policy versus I/O, table-owned writes, transactions,
  identity, ordering, retries, partial success, and compatibility where relevant.
  Prefer the smallest correct reuse path and explain meaningful tradeoffs.
- During planning, label illustrative code as proposed. During implementation
  review, show short actual excerpts and source links from the reviewed
  revision. Include heads/bases and relevant unpublished changes; inspect
  stacked MRs against their actual bases.
- Connect each important rule to a failure case, the enforcing code, validation
  evidence, and remaining gaps. Distinguish existing behavior, proposals,
  inferences, and verified outcomes.
- Keep prose concise and use diagrams to explain relationships rather than
  decorate the page. Avoid repeated summaries and chronological agent logs.

Check HTML structure, anchors, source links, and factual consistency. These
artifact checks do not establish that the application works. Report application
tests separately; do not run unrelated tests merely to populate the document.
Screenshot validation of the walkthrough itself is not required by the skill.

## Preview and validation handoff

For cloud validation, name the runtime in the buddy brief (`dev-store`,
`live`, `mock`, or `none`) and use the shared Cursor-agent runbook. Honor the
already-selected runtime and Dev Store; the personal no-substitution rule above
applies if setup fails. Planning and documentation need no app runtime.

Use infrastructure-owned tailnet routes and the skill's link tooling. Verify
the actual page and backend requests, include access prerequisites and fixtures
without secrets, and keep the environment available for the agreed testing
window. If access expires, restore and reverify it before presenting a usable
link. Disclose when independent verification is blocked and proof comes only
from agent artifacts. Never invent a URL, start a tunnel, or alter its owner.

Each brief states purpose, scope, approved plan, corrections, base/candidate
SHA, relevant code, numbered acceptance cases, runtime/data, allowed side
effects, expected artifacts, and exclusions. Include the applicable personal
cloud-facing rules directly in the brief. The buddy follows its brief and does
not load `cloud-buddy` or `validate` as a parent orchestrator.

Agent idleness is not acceptance. Scheduled monitoring is opt-in. After merge
and verified deployment, offer the repository's production watch under its
normal authorization rules.
