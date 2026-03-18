#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

FORCE=0

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--force] <obsidian-vault-path> [bundle-folder-name]

Examples:
  $(basename "$0") "$HOME/Documents/Obsidian Vault"
  $(basename "$0") "$HOME/Documents/Obsidian Vault" "Codex-Helper"
  $(basename "$0") --force "$HOME/Documents/Obsidian Vault" "Codex-Helper"

Options:
  --force      Overwrite an existing bundle folder
  -h, --help   Show help
USAGE
}

while (($# > 0)); do
  case "$1" in
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

VAULT_PATH="$1"
BUNDLE_NAME="${2:-Codex-Helper}"
TARGET_DIR="${VAULT_PATH}/${BUNDLE_NAME}"

mkdir -p "${VAULT_PATH}"

if [[ -e "${TARGET_DIR}" && "${FORCE}" -eq 0 ]]; then
  printf 'Target already exists: %s\n' "${TARGET_DIR}" >&2
  printf 'Re-run with --force to overwrite.\n' >&2
  exit 1
fi

rm -rf "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}"

cp -R "${REPO_ROOT}/for_obsidian/." "${TARGET_DIR}/"

printf 'Exported Obsidian bundle to: %s\n' "${TARGET_DIR}"
printf 'Open your vault and browse from 00_Home.md\n'
