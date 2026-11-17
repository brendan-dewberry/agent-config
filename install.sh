#!/usr/bin/env bash
set -euo pipefail

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
target_dir=$HOME
dry_run=false
allow_backup=false

usage() {
  cat <<'USAGE'
Usage: ./install.sh [--dry-run] [--backup] [--target DIRECTORY]

Create links for shared instructions, workflows, skills, and executable scripts.
If TARGET/Repo/redo is a checkout, also link and locally exclude its personal
instructions and legacy workflow paths.
Existing files cause installation to stop unless --backup is supplied.
--dry-run prints the plan without changing files.
--target installs into another home directory, useful for a preview or test.
USAGE
}

while (($#)); do
  case "$1" in
    --dry-run) dry_run=true; shift ;;
    --backup) allow_backup=true; shift ;;
    --target)
      if (($# < 2)); then usage >&2; exit 2; fi
      target_dir=$2
      shift 2
      ;;
    --help|-h) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ ! -d "$target_dir" ]]; then
  printf 'Target must be an existing directory: %s\n' "$target_dir" >&2
  exit 2
fi
target_dir=$(cd -- "$target_dir" && pwd -P)
sources=()
destinations=()

add_link() {
  sources+=("$1")
  destinations+=("$target_dir/$2")
}

add_link "$repo_dir/instructions/AGENTS.md" .agents/AGENTS.md
add_link "$repo_dir/instructions/AGENTS.md" .codex/AGENTS.md
add_link "$repo_dir/instructions/AGENTS.md" .claude/CLAUDE.md
add_link "$repo_dir/workflows/redo-development.md" .agents/workflows/redo-development.md

redo_checkout="$target_dir/Repo/redo"
redo_paths=(docs/agentic-development-workflow.local.md AGENTS.local.md)
redo_sources=("$repo_dir/workflows/redo-development.md" "$repo_dir/instructions/redo.md")
redo_exclude_paths=()
redo_exclude_file=
if [[ -e "$redo_checkout/.git" ]]; then
  for i in "${!redo_paths[@]}"; do
    redo_path=${redo_paths[$i]}
    if git -C "$redo_checkout" ls-files --error-unmatch -- "$redo_path" >/dev/null 2>&1; then
      printf 'Refusing to replace tracked file: %s/%s\n' "$redo_checkout" "$redo_path" >&2
      exit 1
    fi
    if ! git -C "$redo_checkout" check-ignore -q -- "$redo_path"; then
      redo_exclude_file=$(git -C "$redo_checkout" rev-parse --git-path info/exclude)
      if [[ "$redo_exclude_file" != /* ]]; then redo_exclude_file="$redo_checkout/$redo_exclude_file"; fi
      printf 'Locally exclude: %s in %s\n' "$redo_path" "$redo_exclude_file"
      redo_exclude_paths+=("$redo_path")
    fi
    add_link "${redo_sources[$i]}" "Repo/redo/$redo_path"
  done
fi

for skill_dir in "$repo_dir"/skills/*; do
  [[ -f "$skill_dir/SKILL.md" ]] || continue
  skill_name=${skill_dir##*/}
  add_link "$skill_dir" ".agents/skills/$skill_name"
  add_link "$skill_dir" ".claude/skills/$skill_name"
  add_link "$skill_dir" ".cursor/skills/$skill_name"
done

for script_path in "$repo_dir"/scripts/*; do
  [[ -f "$script_path" && -x "$script_path" ]] || continue
  add_link "$script_path" ".local/bin/${script_path##*/}"
done

is_installed() {
  [[ -L "$1" && "$(readlink "$1")" == "$2" ]]
}

conflicts=false
for i in "${!sources[@]}"; do
  source_path=${sources[$i]}
  destination=${destinations[$i]}
  parent_dir=$(dirname -- "$destination")
  while [[ "$parent_dir" != "$target_dir" ]]; do
    if [[ ( -e "$parent_dir" || -L "$parent_dir" ) && ! -d "$parent_dir" ]]; then
      printf 'Blocked parent directory: %s\n' "$parent_dir" >&2
      conflicts=true
      break
    fi
    parent_dir=$(dirname -- "$parent_dir")
  done
  if is_installed "$destination" "$source_path"; then
    printf 'Already linked: %s\n' "$destination"
    continue
  fi
  if [[ -e "$destination" || -L "$destination" ]]; then
    if "$allow_backup"; then
      printf 'Back up: %s\n' "$destination"
    else
      printf 'Conflict: %s (use --backup to preserve and replace it)\n' "$destination" >&2
      conflicts=true
    fi
  fi
  printf 'Link: %s -> %s\n' "$destination" "$source_path"
done

if "$conflicts"; then exit 1; fi
if "$dry_run"; then exit 0; fi

if ((${#redo_exclude_paths[@]})); then
  mkdir -p -- "$(dirname -- "$redo_exclude_file")"
  {
    printf '\n# Personal Redo configuration\n'
    printf '/%s\n' "${redo_exclude_paths[@]}"
  } >> "$redo_exclude_file"
fi

backup_dir=
for i in "${!sources[@]}"; do
  source_path=${sources[$i]}
  destination=${destinations[$i]}
  if is_installed "$destination" "$source_path"; then continue; fi
  if [[ -e "$destination" || -L "$destination" ]]; then
    if [[ -z "$backup_dir" ]]; then
      backup_root="$target_dir/.local/state/agent-config/backups"
      mkdir -p -- "$backup_root"
      backup_dir=$(mktemp -d "$backup_root/$(date +%Y%m%d-%H%M%S).XXXXXX")
    fi
    relative_path=${destination#"$target_dir/"}
    backup_path="$backup_dir/$relative_path"
    mkdir -p -- "$(dirname -- "$backup_path")"
    mv -- "$destination" "$backup_path"
  fi
  mkdir -p -- "$(dirname -- "$destination")"
  ln -s -- "$source_path" "$destination"
done

if [[ -n "$backup_dir" ]]; then printf 'Backups saved in: %s\n' "$backup_dir"; fi
printf 'Installation complete. Start a new agent chat to load the instructions.\n'
