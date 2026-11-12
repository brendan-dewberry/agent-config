# Agent configuration

Brendan's shared agent instructions, skills, and personal scripts. Edit the
files in this repository and use Git to track changes over time.

## Contents

- `instructions/AGENTS.md`: shared personal instructions, initially copied from
  the existing Codex configuration.
- `workflows/redo-development.md`: canonical personal Redo development workflow.
- `skills/`: reusable skills. Each imported skill includes its source and
  license so upstream updates can be reviewed deliberately.
- `scripts/`: personal command-line tools. Executable files are installed into
  `$HOME/.local/bin`.
- `config/`: selected agent settings and setup notes.
- `install.sh`: creates links from agent configuration locations to this repo.

## Installed skills

| Skill | Purpose | Dependencies |
| --- | --- | --- |
| `unslop` | Remove AI writing patterns from prose | None |
| `grill-me` | Interview you to sharpen a plan or design | `grilling` |
| `grill-with-docs` | Interview you while capturing glossary terms and architectural decisions | `grilling`, `domain-modeling` |
| `grilling` | Shared interview procedure | None |
| `domain-modeling` | Clarify domain terminology and document decisions | Bundled glossary and ADR formats |
| `redo-agents-api` | Inspect and manage Redo Agents through its authenticated HTTP API | Local Redo Agents API key |
| `launchdarkly` | Read, evaluate and update Redo flags through the LaunchDarkly REST API | AWS CLI production profile or exported LaunchDarkly access token |
| `rmr-engineer` | Run selected RMR tickets locally through architecture, build, proof, Slack review handoff, one human release gate, merge, monitoring and cleanup | Linear/GitLab access, Patch's Slack bot connection or token file, and the product checkout's engineering skills |

Start a task with `Use RMR Engineer to work on RMR-123`, or continue it with
`Use RMR Engineer to resume RMR-123`. This is an opt-in local Codex workflow.
Its task plan stays with local task output; the reusable policy stays here.
It proceeds through architecture, implementation and CI preparation, then
waits for approval of the proven candidate and its release plan. Helm and
Cursor BDK are not required.

Use `$grill-me` or `$grill-with-docs` in Codex. In Claude Code and Cursor,
select the matching skill from the slash-command menu. Both entry points are
explicitly invoked; their dependencies retain the upstream activation settings.
`grill-with-docs` stores personal glossaries and architectural decision records
under `<repo-root>/.agent-notes/domain-modeling/`. Before writing, it adds
`/.agent-notes/` to the repository's local `.git/info/exclude` and verifies the
output paths are ignored. These notes stay out of project commits and merge
requests. Existing tracked team documentation remains reference material.

The skills are editable copies, linked from this repository. They do not update
themselves from upstream. Each `SOURCE.md` records the imported revision.

## Install

Clone this private repository using your authenticated GitHub account:

```bash
gh repo clone brendan-dewberry/agent-config "$HOME/Repo/agent-config"
cd "$HOME/Repo/agent-config"
./install.sh --dry-run
./install.sh
```

If files already occupy an installation path, the installer stops before
changing any files. To back them up and replace them with links:

```bash
./install.sh --dry-run --backup
./install.sh --backup
```

Backups are stored under `$HOME/.local/state/agent-config/backups/`, preserving
the original relative paths. The installer prints the backup directory.
Existing unrelated skills stay in their own directories.

## Installed paths

| Path | Repository source |
| --- | --- |
| `$HOME/.agents/AGENTS.md` | `instructions/AGENTS.md` |
| `$HOME/.codex/AGENTS.md` | `instructions/AGENTS.md` |
| `$HOME/.claude/CLAUDE.md` | `instructions/AGENTS.md` |
| `$HOME/.agents/workflows/redo-development.md` | `workflows/redo-development.md` |
| `$HOME/.agents/skills/<name>` | `skills/<name>/` |
| `$HOME/.claude/skills/<name>` | `skills/<name>/` |
| `$HOME/.cursor/skills/<name>` | `skills/<name>/` |
| `$HOME/.local/bin/<name>` | Executable files in `scripts/` |

Codex discovers skills through `.agents/skills`. Claude and Cursor get their
own skill links. For Cursor instructions, follow `config/README.md`.
Start a new chat after changing instructions so the agent loads the new content.

If `$HOME/Repo/redo` is a checkout, the installer also links its existing
`docs/agentic-development-workflow.local.md` path to the canonical workflow. It
ensures that path is locally ignored, refuses to replace a tracked file, and
preserves an existing local file when `--backup` is supplied. If Redo is absent,
it only installs the shared workflow under `.agents/workflows`.

Edit `workflows/redo-development.md` here to maintain the workflow. Its
repository-relative paths refer to the active Redo checkout, so it continues
using that checkout's managed skills. Include the applicable workflow in cloud
handoff briefs because Redo's Git history does not carry it.

The workflow selects a task type before applying development stages.
Investigations stay read-only. Data cleanup, backfills and manage scripts use
a short plan, local editing, a dry run and focused validation. All Bazel,
builds, types, lint, generation and application tests run in Cloud. Choose
Cloud checks without a full app stack or Cloud runtime proof using the script,
services or UI required by the change. Local read-only Waypoint queries can
provide required database evidence through an existing approved client.
Product changes retain architecture review; explicitly selected RMR Engineer
tickets retain their own release policy. Production data writes still require
authorization for the specific repair.

For example, "Use data maintenance to backfill this existing field" selects
local script editing and focused Cloud checks. An investigation selects the
read-only path automatically; it does not need a separate workflow invocation.

## Make changes

Edit the original files in this repository. Existing links expose the edits
immediately; run `./install.sh` again after adding a skill or executable script.
Running the installer again leaves links that already point here in place.

Review and commit changes, then push them to GitHub. On another machine, pull
the repository and rerun the installer. This is an explicit Git workflow.

The initial instructions preserve the existing Redo preferences and absolute
paths. Review those paths if using a different home directory or checkout.
Personal configuration can be adapted here without adding files to Redo.

## Restore an existing file

Remove the installed link at the specific path you want to restore, then move
that path's original file from the printed backup directory back into place.
Keep the repository at its current location while its links are installed.
