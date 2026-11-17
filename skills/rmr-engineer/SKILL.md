---
name: rmr-engineer
description: Default workflow for new Redo product-development work, including bug fixes. Runs architecture, implementation, scoped proof, human release approval, merge, monitoring and cleanup. Also resumes explicitly selected RMR Engineer tasks. Investigations, manage scripts, data maintenance, instructions/configuration and other selected or established workflows keep their own paths.
---

# RMR Engineer

Use this workflow by default for new Redo product-development work, when the
user selects it, or when continuing a task already using it. Keep investigations,
manage scripts, data maintenance and instructions/configuration on their separate
paths. Honor another explicitly selected or already established workflow.
Codex owns the implementation and lifecycle. Read
[the lifecycle](references/lifecycle.md) at entry and resume. Start the record
from [the task template](assets/task-plan.md).

## Start or resume

1. Fetch the actual Linear ticket, comments, attachments and linked work. Read
   existing task records and search GitLab for open or merged MRs before creating
   work. Reuse the existing implementation when appropriate. A queue listing or
   label does not establish that another agent has stopped working.
2. Inspect the selected checkout's branch, status, AGENTS instructions, domain
   notes and relevant code. Preserve unrelated work. Use one task checkout and
   implementation owner. Codex writes code; validation helpers retain their
   existing restricted roles.
3. Maintain one plan.md and its readable architecture/proof view in the local
   task output directory. Reuse an existing location. Record ticket, stage,
   scope, SHA, decisions, evidence, approval and next action. Keep task records
   outside agent-config and product commits.
4. Reconcile that record with current Linear, Git, MR, CI and deployment evidence.
   Continue the next incomplete step. A checkpoint is a claim to verify.

## Local tools

Use existing integrations and repository skills. Discover actual capabilities
instead of inventing tool names or assuming configured access works.

| Responsibility | Existing procedure |
| --- | --- |
| Ticket/context | Connected Linear tools and current ticket/comments |
| Plan/proof view | engineering-plan guidance and the checkout's architecture-review skill |
| Builds/tests/runtime | cloud-buddy skill at the chosen validation depth; selected environment |
| Draft MR | create-pr skill |
| CI/reviews | ci-fix and watch-pr skills |
| Review handoff | Patch's authenticated Slack connection or local sender, #rmr-eng, and the lifecycle's two-line post |
| Production observation | watch-prod skill, deployment evidence and granted Datadog tools |
| Feature switches | Existing product flag framework and granted provider tools |

Read each needed skill before use. Include personal code-owner and environment
rules in validation briefs. No new implementation agent, SDK, controller,
database, ticket poller or service is required. Helm, hosted Work startup,
ledger tools, lessons and publication are not dependencies of this local flow.

Choose checks and proof using the shared workflow's
[validation and database-access policy](../../workflows/redo-development.md#choose-validation-depth-and-data-access).
All application builds and checks stay in Cloud. A script or database readback
can prove a backend change without starting the UI. Use browser proof when the
acceptance requirements need it, and obtain separate Waypoint evidence when
required performance measurements are unavailable through the Cloud connection.

Use an authenticated automation identity for MR authorship when available and
verify the actual provider identity. Check the intended human's eligibility to
approve early. If the author and approver are the same and the provider refuses
approval, record that integration gap; do not simulate approval or change review
rules. A Redo Agent display name alone does not authenticate a GitLab client.
Managed bot credentials may require a supported local connection or a separately
authorized credential. Do not export protected server credentials or broaden
access as an implementation shortcut.

## Authority for this workflow

The implementation assignment authorizes research, automatic architecture review,
scoped coding/repairs, validation, commits/pushes, a draft MR, review-thread
handling, the required Slack review handoff, marking ready and required CI
preparation. Once checks pass, release an existing draft pipeline using the
repository's normal label and gate-retry procedure. Do not request separate plan
or CI permission for routine progress.
Explicit task restrictions still apply.

Features can use automatic architecture review when the lifecycle's evidence
criteria pass, requirements are sourced and the implementation assignment is
authorized. Record the verdict and rationale; honor unresolved human choices
and an explicit request for manual plan review.

There is one planned human decision gate: approve the proven candidate and its
release plan. It authorizes merge, specified rollout/rollback, monitoring and
the narrowly defined mechanical cleanup in that plan. Starting work is not
that approval. Follow the lifecycle's evidence and invalidation rules. Provider
permissions and mandatory reviews remain requirements; do not bypass them or
create a human approval with agent credentials.

## Continuation and reporting

Continue authorized stages until the human gate, a real blocker or completion.
Use existing waiters while the session is active. On interruption, record pending
waits, provider IDs and next action. Resume with `Use RMR Engineer to resume
RMR-123` and reconcile providers before effects. Do not claim the laptop will
wake or continue after the session stops.

Report current stage, completed evidence, blocker/next action and any needed
human decision. Distinguish implementation, green CI, merge, deployment, actual
feature exposure and cleanup. Completion requires the agreed release,
observation and cleanup requirements to be verified.

Post a short Linear implementation update on pickup and material stage changes,
with the current stage, MR when available and next action. Reuse the local
workflow's comment on resume; skip unchanged status polls. Verify the saved body
and retain its comment ID in the task record. Use the authenticated identity
without implying that it is the hosted RMR Engineer bot.

When the candidate is ready for review, post the lifecycle's two-line request
to #rmr-eng before waiting for approval. Keep proof and status details on the
MR. Record the Slack permalink and candidate SHA privately. A local/chat update
alone does not complete this handoff.

For a local Patch token file, use [the Slack sender](scripts/slack-review.py).
Run `--token-file <path> --check` first. After checking the task receipt and
channel for duplicates, use `--post --title <actual-title> --mr-url <verified-lgtm-url>
--mr-iid <iid>` with that token file. Do not add engineer tags. Use
`--thread-ts <ts>` for an update in the existing thread. Keep the token outside
Git; never pass its value in arguments or chat. Save the returned receipt and
read the message back through Slack. The sender verifies Patch's user/workspace
identity and never retries a post automatically.
