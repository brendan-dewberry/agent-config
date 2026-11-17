---
name: orchestrator
description: >-
  Coordinates a task through shared planning, delegation, integration and
  completion. Use when the user asks to use an orchestrator, act as the
  orchestrator, or orchestrate a task or existing agent chats. Do not activate
  for conceptual questions about orchestration or requests to document it.
---

# Orchestrator

Own the requested outcome and the combined plan. Delegates own detailed plans
and execution within their assigned areas. Collect their results, reconcile
dependencies, and report the combined outcome to the user.

Keep this workflow in instructions, task records and existing agent tools.
It does not call for a new controller, scheduler or application service.

## Establish the assignment

Read the user's objective, existing decisions, applicable repository rules and
selected development workflow. Reuse existing owners, chats, plans and test
environments. Inspect current work before redistributing it.

Define the requested completion point. Research, an implementation, a reviewed
MR and a release are different outcomes. If implementation is requested,
planning is an intermediate milestone; own the transition to implementation.
Preserve existing approvals and ask only for missing decisions that affect the
work. This skill adds no routine human approval gate and grants no release or
production-write permission.

For work spanning several delegates or turns, maintain one small task record
in the existing task output or agreed tracker. Include:

- The outcome, acceptance criteria and shared decisions.
- Each workstream's owner, selected model and agent or chat identifier.
- Its dependencies and, for code, checkout, branch and parent commit.
- Its current phase, evidence, blocker and next action.
- How results will be collected and whether monitoring is active.

Keep plans and evidence in artifacts; return concise summaries to the
orchestrator. Preserve the task record's location in handoffs and compaction.

## Plan together

Scale planning to the work. A small, well-understood task can proceed from a
short brief. For substantial work:

1. Set the initial scope, ownership, acceptance criteria, known contracts and
   dependency order. Identify what delegates need to investigate.
2. Have delegates inspect their area and propose the local implementation and
   validation. They should identify assumptions and effects on other owners.
3. Reconcile their proposals into the combined plan. Resolve overlapping
   changes, shared contracts and sequencing before dependent implementation.
4. Continue the owners into implementation and validation within the approved
   scope. Keep the same worker when its accumulated context remains useful.

Delegates decide local details within the contract. A change to shared
architecture, another owner's interface or agreed scope returns to the
orchestrator for coordination. Bring the user a consolidated recommendation
when a decision falls outside the authorized scope. Follow any architecture
review requirements of the selected development workflow.

Do not require every worker to rediscover settled decisions. Share the updated
contract with affected owners when findings change the plan.

## Choose workers and models

Use the smallest useful set of workers, often two or three for implementation.
Increase concurrency when tasks are independent or the user requests it.
Parallel research can establish facts before shared implementation is ready.
Sequence work that depends on an unsettled contract or touches the same files.

| Work | Preferred worker |
| --- | --- |
| A bounded investigation, review or implementation returned to the parent | Native subagent |
| An ongoing MR or workstream the user will revisit and steer directly | Separate chat, when the user has requested one |
| An already-running workstream with useful context | Its existing owner |

A separate chat is useful for independent ownership and lifecycle. Native
subagents already have separate context and may support follow-up work.
Discover the host's capabilities before assuming either requires a new chat.
Create user-owned chats only when explicitly requested. Respect each tool's
authorization rules for messaging existing chats. Reading this skill alone
does not authorize delegation for an unrelated task.

Assign checkout and file ownership explicitly. A new chat does not isolate
files. Preserve existing changes and follow the environment's checkout rules.
Give shared code one owner and coordinate changes through that owner.

Use explicit model selection when starting or continuing delegated work:

- In Codex, use Sol or Astra for orchestration, Luna for narrow tasks, and Sol
  for demanding implementation, debugging or analysis. Escalate Luna to Sol
  when needed. Use Astra for a delegate only when Brendan explicitly chooses it.
- In Claude Code, absent a user choice, start with Sonnet or Opus coordinating,
  Haiku for narrow tasks, and Sonnet for implementation. Adjust to the actual
  task and models available on that host.
- Resolve model identifiers from the current host or tool catalog and record
  the selected model. If setting a model requires fresh context, supply a
  concise handoff instead of a history fork that inherits the parent model.

Explicit user choices take precedence. Preserve any separately selected Cloud
Buddy provider or model and its role in the development workflow.

## Dispatch a usable brief

Give each delegate enough context to work independently. Include these details
when relevant, without sending the full project history:

```text
Outcome and current phase:
Owner and selected model:
Owned files, checkout, branch and parent commit:
Dependencies and settled shared contracts:
Starting evidence and relevant artifacts:
Applicable workflow and environment:
Acceptance criteria and required validation:
Expected handoff and next milestone:
```

The handoff should identify what changed or was learned, the artifact or commit
that contains it, validation evidence, unresolved issues and the next action.
State whether this assignment is research, planning or implementation. Keep
any existing approval or environment restrictions in the brief.

## Collect, review and continue

Before dispatching, establish how the host returns completion and attention
events. Read [Host coordination](references/host-coordination.md) when choosing
between native agents and separate chats or setting up their result collection.

After dispatching, stay responsible for the work:

1. Wait for results or requests for attention with the host's supported tools.
   Batch independent waits and carry forward cursors or task IDs. Use bounded
   waits that let you remain responsive to the user.
2. Inspect each result and its evidence. An idle worker or final message means
   its turn ended; check which acceptance criteria it actually satisfied.
3. Reconcile the task record. Distinguish a completed plan, implementation,
   passed validation, review readiness and release.
4. Send necessary follow-up work within the authorized scope. Resolve routine
   technical questions, continue after intermediate milestones and unblock
   dependent owners when their prerequisites are ready.
5. Review the combined result. For stacked code changes, verify current parent
   commits and collect validation for the integrated candidate. Earlier evidence
   remains evidence for the earlier candidate. Repeat checks when changes or
   unresolved concerns warrant it.

Do not end the coordination turn merely because workers launched or produced
plans. Continue until the requested outcome is accounted for, a concrete user
decision or external blocker prevents progress, or the user changes the task.
An unattended handoff is valid only when a supported continuation mechanism
has actually been established. A promise to monitor is not that mechanism.

Answer status questions briefly and continue the active assignment. On an
interruption or task change, preserve the checkpoint and describe any change
to monitoring when relevant. On resume, inspect current work before dispatching
duplicates. Carry forward the user's instructions from other authorized chats.

## Report to the user

Report meaningful completions, changed dependencies and decisions that need
the user. Avoid repeating unchanged snapshots or forwarding every worker log.
Consolidate questions and resolve those already answered by the approved plan.

The final response must stand alone: state the outcome, remaining work or
blocker, evidence and artifact links, and whether any work is still active.
Never imply background monitoring after the turn unless its continuation
mechanism is confirmed. Keep the requested completion point visible so a
planning handoff cannot be mistaken for release readiness.
