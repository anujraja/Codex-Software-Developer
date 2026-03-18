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
CACHE_ROOT="${CODEX_HOME}/tmp/codex-helper-skill-link-cache"

FORCE=0
DRY_RUN=0
CUSTOM_ONLY=0
CATALOG_ONLY=0
INSTALL_CUSTOM=1
INSTALL_CATALOG=1

LINKED_AGENTS=0
SKIPPED_AGENTS=0
LINKED_SKILLS=0
SKIPPED_SKILLS=0

usage() {
  cat <<USAGE
Usage: $(basename "$0") [options]

Creates symlinks from this repo into your local Codex folders.

Options:
  --force         Replace existing files/directories at the destination
  --dry-run       Show what would happen without writing
  --custom-only   Link only repo custom assets (.codex/agents + .agents/skills)
  --catalog-only  Link only canonical assets (knowledge/agents + knowledge/skills)
  SKILL_TARGET_DIR env override is respected.
  Default auto-resolution: \$CODEX_HOME/skills if present, else ~/.agents/skills

Notes:
  - Catalog skills are linked via generated cache directories at:
    \$CODEX_HOME/tmp/codex-helper-skill-link-cache
  - Custom skills remain direct symlinks to .agents/skills/*
USAGE
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

link_agent_file() {
  local src_file="$1"
  local src_label="$2"
  local name
  local dst

  name="$(basename "${src_file}")"
  dst="${AGENT_TARGET_DIR}/${name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    printf 'Skipping existing %s agent target: %s\n' "${src_label}" "${dst}"
    SKIPPED_AGENTS=$((SKIPPED_AGENTS + 1))
    return
  fi

  rm -rf "${dst}"
  ln -s "${src_file}" "${dst}"
  printf 'Linked %s agent: %s -> %s\n' "${src_label}" "${dst}" "${src_file}"
  LINKED_AGENTS=$((LINKED_AGENTS + 1))
}

link_custom_skill_dir() {
  local src_dir="$1"
  local name
  local dst

  name="$(basename "${src_dir}")"
  dst="${SKILL_TARGET_DIR}/${name}"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    printf 'Skipping existing custom skill target: %s\n' "${dst}"
    SKIPPED_SKILLS=$((SKIPPED_SKILLS + 1))
    return
  fi

  rm -rf "${dst}"
  ln -s "${src_dir}" "${dst}"
  printf 'Linked custom skill: %s -> %s\n' "${dst}" "${src_dir}"
  LINKED_SKILLS=$((LINKED_SKILLS + 1))
}

link_catalog_skill_file() {
  local src_file="$1"
  local name
  local dst
  local wrapper_dir
  local wrapper_file

  name="$(basename "${src_file}" .md)"
  dst="${SKILL_TARGET_DIR}/${name}"
  wrapper_dir="${CACHE_ROOT}/${name}"
  wrapper_file="${wrapper_dir}/SKILL.md"

  if [[ -e "${dst}" && "${FORCE}" -eq 0 ]]; then
    printf 'Skipping existing catalog skill target: %s\n' "${dst}"
    SKIPPED_SKILLS=$((SKIPPED_SKILLS + 1))
    return
  fi

  rm -rf "${wrapper_dir}"
  mkdir -p "${wrapper_dir}"
  write_canonical_skill_file "${src_file}" "${wrapper_file}" "${name}"

  rm -rf "${dst}"
  ln -s "${wrapper_dir}" "${dst}"
  printf 'Linked catalog skill: %s -> %s\n' "${dst}" "${wrapper_dir}"
  LINKED_SKILLS=$((LINKED_SKILLS + 1))
}

while (($# > 0)); do
  case "$1" in
    --force)
      FORCE=1
      ;;
    --dry-run)
      DRY_RUN=1
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

CATALOG_AGENT_COUNT="$(count_entries "${CATALOG_AGENT_SRC_DIR}" f '*.toml')"
CATALOG_SKILL_COUNT="$(count_entries "${CATALOG_SKILL_SRC_DIR}" f '*.md')"
CUSTOM_AGENT_COUNT="$(count_entries "${CUSTOM_AGENT_SRC_DIR}" f '*.toml')"
CUSTOM_SKILL_COUNT="$(count_entries "${CUSTOM_SKILL_SRC_DIR}" d '*')"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  printf '[dry-run] Skill target resolved to %s (%s)\n' "${SKILL_TARGET_DIR}" "${SKILL_TARGET_RESOLUTION_REASON}"
  if [[ "${INSTALL_CATALOG}" -eq 1 ]]; then
    printf '[dry-run] Would link %s catalog agents from %s to %s\n' "${CATALOG_AGENT_COUNT}" "${CATALOG_AGENT_SRC_DIR}" "${AGENT_TARGET_DIR}"
    printf '[dry-run] Would link %s catalog skills from %s to %s (via %s)\n' "${CATALOG_SKILL_COUNT}" "${CATALOG_SKILL_SRC_DIR}" "${SKILL_TARGET_DIR}" "${CACHE_ROOT}"
  fi
  if [[ "${INSTALL_CUSTOM}" -eq 1 ]]; then
    printf '[dry-run] Would link %s custom agents from %s to %s\n' "${CUSTOM_AGENT_COUNT}" "${CUSTOM_AGENT_SRC_DIR}" "${AGENT_TARGET_DIR}"
    printf '[dry-run] Would link %s custom skills from %s to %s\n' "${CUSTOM_SKILL_COUNT}" "${CUSTOM_SKILL_SRC_DIR}" "${SKILL_TARGET_DIR}"
  fi
  exit 0
fi

printf 'Skill target resolved to %s (%s)\n' "${SKILL_TARGET_DIR}" "${SKILL_TARGET_RESOLUTION_REASON}"

mkdir -p "${AGENT_TARGET_DIR}" "${SKILL_TARGET_DIR}" "${CACHE_ROOT}"

if [[ "${INSTALL_CATALOG}" -eq 1 ]]; then
  while IFS= read -r agent_file; do
    [[ -z "${agent_file}" ]] && continue
    link_agent_file "${agent_file}" "catalog"
  done < <(find "${CATALOG_AGENT_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort)

  while IFS= read -r skill_file; do
    [[ -z "${skill_file}" ]] && continue
    link_catalog_skill_file "${skill_file}"
  done < <(find "${CATALOG_SKILL_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.md' | sort)
fi

if [[ "${INSTALL_CUSTOM}" -eq 1 ]]; then
  while IFS= read -r agent_file; do
    [[ -z "${agent_file}" ]] && continue
    link_agent_file "${agent_file}" "custom"
  done < <(find "${CUSTOM_AGENT_SRC_DIR}" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort)

  while IFS= read -r skill_dir; do
    [[ -z "${skill_dir}" ]] && continue
    link_custom_skill_dir "${skill_dir}"
  done < <(find "${CUSTOM_SKILL_SRC_DIR}" -mindepth 1 -maxdepth 1 -type d | sort)
fi

printf 'Symlink setup complete.\n'
printf 'Linked agents: %s; skipped agents: %s\n' "${LINKED_AGENTS}" "${SKIPPED_AGENTS}"
printf 'Linked skills: %s; skipped skills: %s\n' "${LINKED_SKILLS}" "${SKIPPED_SKILLS}"
