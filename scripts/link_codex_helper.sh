#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
AGENT_TARGET_DIR="${AGENT_TARGET_DIR:-${CODEX_HOME}/agents}"
SKILL_TARGET_DIR="${SKILL_TARGET_DIR:-${HOME}/.agents/skills}"

FORCE=0

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--force]

Creates symlinks from this repo into your local Codex folders.

Options:
  --force   Replace existing files/directories at the destination
USAGE
}

while (($# > 0)); do
  case "$1" in
    --force)
      FORCE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n\n' "$1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

mkdir -p "${AGENT_TARGET_DIR}" "${SKILL_TARGET_DIR}"

for agent_file in "${REPO_ROOT}"/.codex/agents/*.toml; do
  name="$(basename "${agent_file}")"
  dst="${AGENT_TARGET_DIR}/${name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    printf 'Skipping existing agent symlink target: %s\n' "${dst}"
    continue
  fi

  rm -rf "${dst}"
  ln -s "${agent_file}" "${dst}"
  printf 'Linked agent: %s -> %s\n' "${dst}" "${agent_file}"
done

for skill_dir in "${REPO_ROOT}"/.agents/skills/*; do
  name="$(basename "${skill_dir}")"
  dst="${SKILL_TARGET_DIR}/${name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    printf 'Skipping existing skill symlink target: %s\n' "${dst}"
    continue
  fi

  rm -rf "${dst}"
  ln -s "${skill_dir}" "${dst}"
  printf 'Linked skill: %s -> %s\n' "${dst}" "${skill_dir}"
done

printf 'Symlink setup complete.\n'
