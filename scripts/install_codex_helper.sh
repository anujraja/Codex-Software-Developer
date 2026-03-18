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

CUSTOM_AGENT_SRC_DIR="${REPO_ROOT}/.codex/agents"
CUSTOM_SKILL_SRC_DIR="${REPO_ROOT}/.agents/skills"
CATALOG_AGENT_SRC_DIR="${REPO_ROOT}/knowledge/agents"
CATALOG_SKILL_SRC_DIR="${REPO_ROOT}/knowledge/skills"

GLOBAL_TEMPLATE="${REPO_ROOT}/templates/global-AGENTS.md"
CONFIG_TEMPLATE="${REPO_ROOT}/.codex/config.toml"

FORCE=0
DRY_RUN=0
WITH_GLOBAL_GUIDANCE=0
CUSTOM_ONLY=0
CATALOG_ONLY=0
INSTALL_CUSTOM=1
INSTALL_CATALOG=1

INSTALLED_AGENTS=0
SKIPPED_AGENTS=0
INSTALLED_SKILLS=0
SKIPPED_SKILLS=0

log() {
  printf '==> %s\n' "$*"
}

usage() {
  cat <<USAGE
Usage: $(basename "$0") [options]

Options:
  --force                 Overwrite matching agents/skills (with backup)
  --with-global-guidance  Create or refresh Codex Helper guidance block in ~/.codex/AGENTS.md
  --dry-run               Show what would happen without writing
  --custom-only           Install only repo custom assets (.codex/agents + .agents/skills)
  --catalog-only          Install only canonical assets (knowledge/agents + knowledge/skills)
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

extract_canonical_summary() {
  local src_file="$1"
  local summary
  summary="$(awk '/^## Summary/{getline; print; exit}' "${src_file}" | tr -d '\r')"
  if [[ -z "${summary}" ]]; then
    summary="Imported canonical skill from Codex Helper knowledge catalog."
  fi
  printf '%s' "${summary}"
}

write_canonical_skill_file() {
  local src_file="$1"
  local dst_file="$2"
  local skill_name="$3"
  local summary

  summary="$(extract_canonical_summary "${src_file}")"

  {
    printf -- '---\n'
    printf 'name: %s\n' "${skill_name}"
    printf 'description: >-\n'
    printf '  %s\n' "${summary}"
    printf -- '---\n\n'
    cat "${src_file}"
    printf '\n'
  } > "${dst_file}"
}

count_entries() {
  local path="$1"
  local type_flag="$2"
  local pattern="$3"

  if [[ ! -d "${path}" ]]; then
    printf '0'
    return
  fi

  find "${path}" -mindepth 1 -maxdepth 1 -type "${type_flag}" -name "${pattern}" | wc -l | tr -d '[:space:]'
}

install_agent_file() {
  local src_file="$1"
  local src_label="$2"
  local agent_name
  local dst

  agent_name="$(basename "${src_file}")"
  dst="${AGENT_TARGET_DIR}/${agent_name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    log "Skipping existing ${src_label} agent ${agent_name} (use --force to overwrite)"
    SKIPPED_AGENTS=$((SKIPPED_AGENTS + 1))
    return
  fi

  backup_path "${dst}" "${BACKUP_ROOT}/agents/${agent_name}"
  cp "${src_file}" "${dst}"
  INSTALLED_AGENTS=$((INSTALLED_AGENTS + 1))
  log "Installed ${src_label} agent: ${agent_name}"
}

install_custom_skill_dir() {
  local src_dir="$1"
  local skill_name
  local dst

  skill_name="$(basename "${src_dir}")"
  dst="${SKILL_TARGET_DIR}/${skill_name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    log "Skipping existing custom skill ${skill_name} (use --force to overwrite)"
    SKIPPED_SKILLS=$((SKIPPED_SKILLS + 1))
    return
  fi

  backup_path "${dst}" "${BACKUP_ROOT}/skills/${skill_name}"
  rm -rf "${dst}"
  mkdir -p "${dst}"
  copy_dir_contents "${src_dir}" "${dst}"
  INSTALLED_SKILLS=$((INSTALLED_SKILLS + 1))
  log "Installed custom skill: ${skill_name}"
}

install_catalog_skill_file() {
  local src_file="$1"
  local skill_name
  local dst_dir
  local dst_file

  skill_name="$(basename "${src_file}" .md)"
  dst_dir="${SKILL_TARGET_DIR}/${skill_name}"
  dst_file="${dst_dir}/SKILL.md"

  if [[ -e "${dst_dir}" && "${FORCE}" -eq 0 ]]; then
    log "Skipping existing catalog skill ${skill_name} (use --force to overwrite)"
    SKIPPED_SKILLS=$((SKIPPED_SKILLS + 1))
    return
  fi

  backup_path "${dst_dir}" "${BACKUP_ROOT}/skills/${skill_name}"
  rm -rf "${dst_dir}"
  mkdir -p "${dst_dir}"
  write_canonical_skill_file "${src_file}" "${dst_file}" "${skill_name}"
  INSTALLED_SKILLS=$((INSTALLED_SKILLS + 1))
  log "Installed catalog skill: ${skill_name}"
}

upsert_global_guidance_block() {
  local target_agents_md="$1"
  local start_marker="<!-- CODEX-HELPER START -->"
  local end_marker="<!-- CODEX-HELPER END -->"
  local tmp_file

  if [[ ! -f "${target_agents_md}" ]]; then
    cp "${GLOBAL_TEMPLATE}" "${target_agents_md}"
    log "Created ${target_agents_md} with Codex Helper guidance"
    return
  fi

  if grep -q "${start_marker}" "${target_agents_md}"; then
    backup_path "${target_agents_md}" "${BACKUP_ROOT}/AGENTS.md"
    tmp_file="$(mktemp)"

    awk -v start_marker="${start_marker}" -v end_marker="${end_marker}" -v template_file="${GLOBAL_TEMPLATE}" '
      BEGIN {
        while ((getline line < template_file) > 0) {
          block = block line ORS
        }
        close(template_file)
        replaced = 0
        in_block = 0
      }
      {
        if (index($0, start_marker) > 0) {
          if (!replaced) {
            printf "%s", block
            replaced = 1
          }
          in_block = 1
          next
        }
        if (in_block) {
          if (index($0, end_marker) > 0) {
            in_block = 0
          }
          next
        }
        print
      }
      END {
        if (!replaced) {
          if (NR > 0) {
            printf "\n"
          }
          printf "%s", block
        }
      }
    ' "${target_agents_md}" > "${tmp_file}"

    mv "${tmp_file}" "${target_agents_md}"
    log "Updated Codex Helper guidance block in ${target_agents_md}"
    return
  fi

  backup_path "${target_agents_md}" "${BACKUP_ROOT}/AGENTS.md"
  {
    printf '\n'
    cat "${GLOBAL_TEMPLATE}"
  } >> "${target_agents_md}"
  log "Appended Codex Helper guidance to ${target_agents_md}"
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
    --custom-only)
      CUSTOM_ONLY=1
      ;;
    --catalog-only)
      CATALOG_ONLY=1
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

if [[ "${CUSTOM_ONLY}" -eq 1 && "${CATALOG_ONLY}" -eq 1 ]]; then
  printf 'Cannot combine --custom-only and --catalog-only.\n' >&2
  exit 1
fi

if [[ "${CUSTOM_ONLY}" -eq 1 ]]; then
  INSTALL_CATALOG=0
fi
if [[ "${CATALOG_ONLY}" -eq 1 ]]; then
  INSTALL_CUSTOM=0
fi

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${CODEX_HOME}/backups/codex-helper-${TIMESTAMP}"

CATALOG_AGENT_COUNT="$(count_entries "${CATALOG_AGENT_SRC_DIR}" f '*.toml')"
CATALOG_SKILL_COUNT="$(count_entries "${CATALOG_SKILL_SRC_DIR}" f '*.md')"
CUSTOM_AGENT_COUNT="$(count_entries "${CUSTOM_AGENT_SRC_DIR}" f '*.toml')"
CUSTOM_SKILL_COUNT="$(count_entries "${CUSTOM_SKILL_SRC_DIR}" d '*')"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  log "[dry-run] Skill target resolved to ${SKILL_TARGET_DIR} (${SKILL_TARGET_RESOLUTION_REASON})"
  if [[ "${INSTALL_CATALOG}" -eq 1 ]]; then
    log "[dry-run] Would install ${CATALOG_AGENT_COUNT} catalog agents from ${CATALOG_AGENT_SRC_DIR} to ${AGENT_TARGET_DIR}"
    log "[dry-run] Would install ${CATALOG_SKILL_COUNT} catalog skills from ${CATALOG_SKILL_SRC_DIR} to ${SKILL_TARGET_DIR}"
  fi
  if [[ "${INSTALL_CUSTOM}" -eq 1 ]]; then
    log "[dry-run] Would install ${CUSTOM_AGENT_COUNT} custom agents from ${CUSTOM_AGENT_SRC_DIR} to ${AGENT_TARGET_DIR}"
    log "[dry-run] Would install ${CUSTOM_SKILL_COUNT} custom skills from ${CUSTOM_SKILL_SRC_DIR} to ${SKILL_TARGET_DIR}"
  fi
  log "[dry-run] Would copy config template to ${CODEX_HOME}/config.codex-helper.example.toml"
  if [[ "${WITH_GLOBAL_GUIDANCE}" -eq 1 ]]; then
    log "[dry-run] Would create/update guidance block in ${CODEX_HOME}/AGENTS.md"
  fi
  exit 0
fi

log "Skill target resolved to ${SKILL_TARGET_DIR} (${SKILL_TARGET_RESOLUTION_REASON})"

mkdir -p "${CODEX_HOME}" "${AGENT_TARGET_DIR}" "${SKILL_TARGET_DIR}"

if [[ "${INSTALL_CATALOG}" -eq 1 ]]; then
  log "Installing catalog agents from knowledge/agents"
  while IFS= read -r agent_file; do
    [[ -z "${agent_file}" ]] && continue
    install_agent_file "${agent_file}" "catalog"
  done < <(find "${CATALOG_AGENT_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort)

  log "Installing catalog skills from knowledge/skills"
  while IFS= read -r skill_file; do
    [[ -z "${skill_file}" ]] && continue
    install_catalog_skill_file "${skill_file}"
  done < <(find "${CATALOG_SKILL_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.md' | sort)
fi

if [[ "${INSTALL_CUSTOM}" -eq 1 ]]; then
  log "Installing custom agents from .codex/agents"
  while IFS= read -r agent_file; do
    [[ -z "${agent_file}" ]] && continue
    install_agent_file "${agent_file}" "custom"
  done < <(find "${CUSTOM_AGENT_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort)

  log "Installing custom skills from .agents/skills"
  while IFS= read -r skill_dir; do
    [[ -z "${skill_dir}" ]] && continue
    install_custom_skill_dir "${skill_dir}"
  done < <(find "${CUSTOM_SKILL_SRC_DIR}" -mindepth 1 -maxdepth 1 -type d | sort)
fi

cp "${CONFIG_TEMPLATE}" "${CODEX_HOME}/config.codex-helper.example.toml"
log "Installed config template: ${CODEX_HOME}/config.codex-helper.example.toml"

if [[ "${WITH_GLOBAL_GUIDANCE}" -eq 1 ]]; then
  TARGET_AGENTS_MD="${CODEX_HOME}/AGENTS.md"
  upsert_global_guidance_block "${TARGET_AGENTS_MD}"
fi

log "Install complete"
log "Installed agents: ${INSTALLED_AGENTS}; skipped agents: ${SKIPPED_AGENTS}"
log "Installed skills: ${INSTALLED_SKILLS}; skipped skills: ${SKIPPED_SKILLS}"
log "Backup location (if any files were replaced): ${BACKUP_ROOT}"
log "Verify with: ls ${AGENT_TARGET_DIR} && ls ${SKILL_TARGET_DIR}"
