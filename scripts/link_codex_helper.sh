#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
AGENT_TARGET_DIR="${AGENT_TARGET_DIR:-${CODEX_HOME}/agents}"

if [[ -n "${SKILL_TARGET_DIR:-}" ]]; then
  SKILL_TARGET_RESOLUTION_REASON="SKILL_TARGET_DIR environment override"
elif [[ -d "${CODEX_HOME}/skills" ]]; then
  SKILL_TARGET_DIR="${CODEX_HOME}/skills"
  SKILL_TARGET_RESOLUTION_REASON="existing CODEX_HOME skills directory detected at ${CODEX_HOME}/skills"
else
  SKILL_TARGET_DIR="${HOME}/.agents/skills"
  SKILL_TARGET_RESOLUTION_REASON="fallback to official user-level skills path ~/.agents/skills"
fi

FORCE=0

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--force]

Creates symlinks from this repo into your local Codex folders.

Options:
  --force   Replace existing files/directories at the destination
  SKILL_TARGET_DIR env override is respected.
  Default auto-resolution: \$CODEX_HOME/skills if present, else ~/.agents/skills
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

printf 'Skill target resolved to %s (%s)\n' "${SKILL_TARGET_DIR}" "${SKILL_TARGET_RESOLUTION_REASON}"

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
