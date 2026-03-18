#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_FILE="${REPO_ROOT}/for_obsidian/90_Markdown_Inventory.md"

{
  printf '# Markdown Inventory\n\n'
  printf '_Generated on %s_\n\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
  printf 'This is a full markdown-file inventory for this repository.\n\n'

  printf '## Repository Markdown Files\n\n'
  find "${REPO_ROOT}" -type f -name '*.md' \
    ! -path '*/.git/*' \
    | sed "s|${REPO_ROOT}/||" \
    | sort \
    | while read -r path; do
      printf -- '- `%s`\n' "${path}"
    done
} > "${OUTPUT_FILE}"

printf 'Wrote inventory: %s\n' "${OUTPUT_FILE}"
