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

GLOBAL_TEMPLATE="${REPO_ROOT}/templates/global-AGENTS.md"
CONFIG_TEMPLATE="${REPO_ROOT}/.codex/config.toml"

FORCE=0
DRY_RUN=0
WITH_GLOBAL_GUIDANCE=0

log() {
  printf '==> %s\n' "$*"
}

usage() {
  cat <<USAGE
Usage: $(basename "$0") [options]

Options:
  --force                 Overwrite matching agents/skills (with backup)
  --with-global-guidance  Append Codex Helper guidance block to ~/.codex/AGENTS.md
  --dry-run               Show what would happen without writing
  SKILL_TARGET_DIR        Optional env override for skill install destination
                          Default auto-resolution: \$CODEX_HOME/skills if present, else ~/.agents/skills
  -h, --help              Show help
USAGE
}

copy_dir_contents() {
  local src_dir="$1"
  local dst_dir="$2"

  mkdir -p "${dst_dir}"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a "${src_dir}/" "${dst_dir}/"
  else
    cp -R "${src_dir}/." "${dst_dir}/"
  fi
}

backup_path() {
  local src="$1"
  local dst="$2"

  if [[ -e "${src}" ]]; then
    mkdir -p "$(dirname "${dst}")"
    cp -R "${src}" "${dst}"
  fi
}

while (($# > 0)); do
  case "$1" in
    --force)
      FORCE=1
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    --with-global-guidance)
      WITH_GLOBAL_GUIDANCE=1
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

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${CODEX_HOME}/backups/codex-helper-${TIMESTAMP}"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  log "[dry-run] Skill target resolved to ${SKILL_TARGET_DIR} (${SKILL_TARGET_RESOLUTION_REASON})"
  log "[dry-run] Would copy agents from ${REPO_ROOT}/.codex/agents to ${AGENT_TARGET_DIR}"
  log "[dry-run] Would copy skills from ${REPO_ROOT}/.agents/skills to ${SKILL_TARGET_DIR}"
  log "[dry-run] Would copy config template to ${CODEX_HOME}/config.codex-helper.example.toml"
  if [[ "${WITH_GLOBAL_GUIDANCE}" -eq 1 ]]; then
    log "[dry-run] Would append guidance block to ${CODEX_HOME}/AGENTS.md"
  fi
  exit 0
fi

log "Skill target resolved to ${SKILL_TARGET_DIR} (${SKILL_TARGET_RESOLUTION_REASON})"

mkdir -p "${CODEX_HOME}" "${AGENT_TARGET_DIR}" "${SKILL_TARGET_DIR}"

log "Installing custom agents"
for agent_file in "${REPO_ROOT}"/.codex/agents/*.toml; do
  agent_name="$(basename "${agent_file}")"
  dst="${AGENT_TARGET_DIR}/${agent_name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    log "Skipping existing agent ${agent_name} (use --force to overwrite)"
    continue
  fi

  backup_path "${dst}" "${BACKUP_ROOT}/agents/${agent_name}"
  cp "${agent_file}" "${dst}"
  log "Installed agent: ${agent_name}"
done

log "Installing custom skills"
for skill_dir in "${REPO_ROOT}"/.agents/skills/*; do
  skill_name="$(basename "${skill_dir}")"
  dst="${SKILL_TARGET_DIR}/${skill_name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    log "Skipping existing skill ${skill_name} (use --force to overwrite)"
    continue
  fi

  backup_path "${dst}" "${BACKUP_ROOT}/skills/${skill_name}"
  rm -rf "${dst}"
  mkdir -p "${dst}"
  copy_dir_contents "${skill_dir}" "${dst}"
  log "Installed skill: ${skill_name}"
done

cp "${CONFIG_TEMPLATE}" "${CODEX_HOME}/config.codex-helper.example.toml"
log "Installed config template: ${CODEX_HOME}/config.codex-helper.example.toml"

if [[ "${WITH_GLOBAL_GUIDANCE}" -eq 1 ]]; then
  TARGET_AGENTS_MD="${CODEX_HOME}/AGENTS.md"
  START_MARKER="<!-- CODEX-HELPER START -->"

  if [[ ! -f "${TARGET_AGENTS_MD}" ]]; then
    cp "${GLOBAL_TEMPLATE}" "${TARGET_AGENTS_MD}"
    log "Created ${TARGET_AGENTS_MD} with Codex Helper guidance"
  elif grep -q "${START_MARKER}" "${TARGET_AGENTS_MD}"; then
    log "Global guidance already exists in ${TARGET_AGENTS_MD}"
  else
    {
      printf '\n'
      cat "${GLOBAL_TEMPLATE}"
    } >> "${TARGET_AGENTS_MD}"
    log "Appended Codex Helper guidance to ${TARGET_AGENTS_MD}"
  fi
fi

log "Install complete"
log "Backup location (if any files were replaced): ${BACKUP_ROOT}"
log "Verify with: ls ${AGENT_TARGET_DIR} && ls ${SKILL_TARGET_DIR}"
