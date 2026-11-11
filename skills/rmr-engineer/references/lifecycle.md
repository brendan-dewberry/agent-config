# RMR Engineer lifecycle

This is portable workflow policy. A host supplies ticket access, a checkout,
validation, CI, approval evidence, deployment observation and flag controls.
Verify tool bindings and continuation behavior when moving to another host.

## 1. PRD / Architect

Establish the problem, required behavior, exclusions, acceptance checks,
ownership, existing work and the smallest approach grounded in current code.
Maintain one engineering plan through the task and update its readable view.

Record an automated architecture verdict and rationale for these criteria:

- Requirements and acceptance checks are specific enough to implement.
- For incident fixes, acceptance checks reflect later triage corrections and
  conflicting evidence. State which reported cases are covered and which remain
  unproven.
- Scope is bounded and existing implementations/callers have been researched.
- The approach follows established patterns or explains the necessary deviation.
- Relevant data, authorization, compatibility, retry and failure rules are clear.
  Required migrations and irreversible effects are explicit.
- Validation, switching, rollout, observation and rollback have concrete plans
  using identified existing capabilities. Record any unverified access.
- No unresolved product decision, competing owner or conflicting requirement
  blocks the approach.

Proceed automatically when all applicable checks pass. Research factual unknowns
before asking the user. Ask for unresolved outcomes or consequential choices;
record the answer and update affected scope. Difficult tickets use this same
lifecycle with more research and decisions. Honor requested manual plan review.
Generated recommendations and silence are not human decisions.

This automatic path includes features with sourced requirements and a clear
implementation approach. Under an authorized implementation assignment, passing
the criteria above permits Build and CI without a separate human plan signoff.
Record requirement sources, inspected code, the automated verdict and rationale.
Confidence comes from that evidence, not a percentage or the feature label.

Keep specified product behavior in the requirements and source evidence. Record
supported technical choices in the approach without inventing a human decision
for every implementation choice. Research missing facts; ask for unresolved
product choices, consequential technical uncertainty, effects outside the
assignment or explicitly requested manual architecture review. Planning-only
assignments remain planning-only. The human release gate still applies.

Architecture approval permits build, not release or a claim that proof passed.
Missing access for a later operation blocks that operation; continue independent
authorized work. Resolve release-critical access before requesting the human gate.

## 2. Build & validate

Implement the recorded outcome and necessary prerequisites. Apply the shared
[validation and database-access policy](../../../workflows/redo-development.md#choose-validation-depth-and-data-access).
Record Cloud checks or Cloud runtime proof and why it covers the acceptance
requirements. Start or reuse the helper when code needs checks or execution;
all Bazel, types, lint, generation and tests stay in Cloud. A manage script and
database readback can be sufficient without a full app or UI. Use a browser
when the changed behavior needs it. Preserve any selected runtime/Dev Store.
Codex reviews and commits code and generated patches; validation helpers do
not take over implementation.

Use an existing product feature switch by default, initially off. Record its
key, owner, defaults, targeting, removal condition and guarded paths. Prove that
flag-off preserves existing behavior and flag-on delivers the intended behavior.
A Temporal version marker controls replay compatibility; it is not an operator
feature switch. Keep both responsibilities explicit.

A trivial exception needs a written reason why a switch adds no useful rollout
or rollback control, with no database or consequential workflow change. Diff
size alone does not establish triviality. If a meaningful change cannot be
switched safely, settle its concrete release constraint rather than silently
skipping the requirement.

Run scoped checks and the selected proof using existing skills. Obtain required
Waypoint plans/measurements separately when Cloud/PGMask cannot supply them;
record the gap until that evidence returns. Tie each result to the tested SHA,
environment, fixture, actual test count and evidence. Label
mocked-provider and real integration results accurately. Create/adopt a draft
MR, inspect the complete diff and callers, fix findings and revalidate affected
paths. Keep adjacent work outside scope.

## 3. Prove it and obtain release approval

Complete approval-independent validation and CI. Attach evidence and resolve
review findings. Verify head/target, required child pipelines, conflicts,
discussions and legitimate approval-dependent checks. A pipeline awaiting those
checks is not green.

Present one review package containing:

- MR, candidate SHA, accepted scope and implementation walkthrough.
- Working demonstration or regression proof, with its limits.
- Switch on/off evidence or justified trivial exception.
- CI/review state, remaining provider approvals and evidence gaps.
- Release plan: deployment mechanism, initial exposure, expansion criteria,
  observation window, success/error signals and rollback actions.
- Cleanup plan: winning behavior, removal condition and exact mechanical
  change categories covered by this approval.

### Required Slack review handoff

When the MR is waiting on a person, after its approval-independent checks pass
and proof is attached, post to #rmr-eng, channel C0938J181B8, using the connected
RMR Engineer bot, Patch. Verify the authenticated sender before posting. A
personal Slack connector does not use Patch's identity. If the bot connection
is unavailable locally, record the delivery gap; do not fall back to Brendan's
account unless he explicitly chooses that fallback. Keep the message to two lines:

1. The actual work/MR title, including the ticket identifier. Remove only an
   automatic Draft: prefix.
2. The verified LGTM MR review link.

For now, do not tag engineers in the initial post or thread updates. MRs can be
authored as the same user the workflow would tag. Keep reviewer assignments and
native approval eligibility on the MR and in the task record. Keep summaries, test
counts, SHAs, CI status, blockers, readiness claims, proof/plan links and tooling
details on the MR and in the task record. Do not include them in the channel
message. Release-access setup does not delay an otherwise ready code review.

Check the task's receipt and existing MR review thread before posting. Send one
initial request per MR; put material candidate or readiness updates in that
thread. Do not repost for status polls. Verify the sent message and record its
channel, timestamp, permalink, sender and candidate SHA in the task plan. If sending
fails, record the error and report the handoff as incomplete. Resume from the
receipt rather than assuming a message was delivered. Use a different channel
when the user explicitly selects one.

Obtain the assigned human's approval of that package. Prefer actual native MR
approval; retain actor, source, time, reviewed SHA and plan revision. An explicit
conversation approval can authorize release of the named package, but does not
satisfy a separate mandatory provider review. Never use the agent's provider
approval call to fabricate the user's approval.

Approval covers the candidate, stated rollout/rollback and mechanical cleanup.
New behavior, expanded scope, consequential code changes or a changed release
plan invalidate affected approval. Revalidate any new head and obtain renewed
approval when reviewed behavior or risk changes. Honor valid existing approval.

## 4. CI readiness / Merge

After approval, verify the approved candidate and current provider state.
Complete legitimate approval-sensitive checks with existing CI/MR procedures.
Do not bypass reviews, force merge, mark failures passed or merge a different
head. Scoped repairs follow approval invalidation rules.

Once all required checks and provider approvals are satisfied, request merge
or native auto-merge through the available authorized GitLab path. Verify its
receipt and final merge commit. Observe deployment through existing mechanisms;
a merge or successful build alone does not establish production deployment.

## 5. Monitor

Verify the production deployment contains the merge before exposing the feature.
Apply only targeting/expansion authorized by the release plan through existing
granted controls. Retain change receipts and prior owned targeting for rollback.
A disabled feature has not exercised the new path.

Use Datadog as the default monitoring source. Reuse the actual alert query and
verify cohort and correlation fields on both failure and activity records
before filtering; those fields can differ. Use another UI or workflow history
to answer a specific unresolved question. A separate Temporal login or credential
is not a routine prerequisite when existing telemetry covers the release plan.

Observe the planned population and signals over the agreed window. For a rare
bug, absence of errors without a relevant execution is inconclusive. Distinguish
regression proof from actual production exposure. Mark missing signals
unverified and record actual observation times.

On a plausible regression, pause expansion and follow the approved rollback.
Report evidence and needed human action. Do not improvise unrelated production
repairs. Missing flag, deployment or observation access blocks that operation
without discarding earlier evidence.

## 6. Release / Clean up

Confirm full intended rollout and successful observation before deleting a flag
or behavior path. Partial exposure keeps both paths. Record the winner and
production evidence.

Prepare a scoped cleanup MR removing the approved flag, losing path, test
overrides, temporary copies and markers while preserving the winning behavior.
Validate and run required CI on its current head. The single release gate
covers mechanical cleanup only when its plan explicitly included it and its
removal condition is proven. New behavior/product decisions require renewed
approval.

Honor mandatory provider reviews for cleanup. If they require fresh human
action, report a concrete gap in the one-gate goal; do not bypass them or claim
fully automated cleanup. Archive the provider flag only after deployed code no
longer references it and the approved plan permits that action.

Verify cleanup merge/deployment as applicable. Record receipts and remaining
obligations before closing the ticket. Unfinished work retains an owner and
next action instead of a completion claim.
