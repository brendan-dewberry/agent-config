# Host coordination

Use the capabilities and tool schemas available in the current session.
Version-dependent features in online documentation may not exist on the
installed host. Choose how to collect results before launching workers.

## Codex native subagents

Use the available collaboration tools to spawn, message, wait for and resume
subagents. Their results return to the parent, which reviews and combines them.
A message to an idle agent may not start work; use the host's follow-up or
resume operation when required. Select the delegate model explicitly. Some
hosts allow a model override only with a fresh-context handoff.

Wait for the assigned work before reporting its outcome. Do not assume an
agent completion will start a new parent turn after the parent ends.

## Codex separate chats

Discover the desktop tools for listing, reading, creating, messaging and
waiting on chats. Read an existing owner's current state before sending work.
Use native subagents when a separate user-owned chat has not been requested.

When `wait_threads` is available, use compact snapshots and bounded waits for
the active owners. Carry forward each returned cursor. A wait may return on
the first chat that finishes or needs attention; continue collecting the
remaining owners. Read full chat content only when needed to inspect a result
or resolve uncertainty. Keep approval requests with the user.

Treat completion watching as active work in the current turn unless the host
provides and confirms a separate continuation mechanism. Do not use recurring
automation to follow a single task to completion. Do not ask another chat to
message back as a substitute for result collection when its tools require
separate human authorization to send that message.

## Claude Code

Use native subagents for bounded work within the session. Check current
foreground, background and fork settings before relying on a blocking wait.
Explicitly select the model instead of relying on inheritance. Inspect results
after completion notifications before marking the assignment complete.

For independent sessions, discover supported cross-session messaging and
completion subscriptions. Where available, `notify_when_idle` is a one-time
subscription to a local session becoming idle or exiting. Register it for the
intended assignment, confirm it was accepted, and renew it for follow-up work
when needed. Inbound controls, host lifetime and expiry affect delivery.
Idle is a turn boundary, so inspect the handoff before treating it as success.

Agent teams may help when peers need a shared task list and direct discussion.
Do not enable them solely because there are several tasks. Check the installed
version's resume and completion behavior, and reconcile actual evidence when
task status lags. A framework's plan-approval transition does not establish
that the orchestrator reviewed the plan or that the user approved new scope.

## Official references

Consult these when host behavior is uncertain; do not reread all of them for
every task:

- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)
- [Claude Code cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
- [Claude Code background sessions](https://code.claude.com/docs/en/agent-view)
