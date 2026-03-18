#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_FILE="${REPO_ROOT}/for_obsidian/90_Markdown_Inventory.md"
TARGET_ROOT="${REPO_ROOT}/for_obsidian"

{
  printf '# Markdown Inventory\n\n'
  printf '_Generated on %s_\n\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
  printf 'This is the markdown-file inventory for the Obsidian bundle folder.\n\n'

  printf '## Obsidian Bundle Markdown Files\n\n'
  find "${TARGET_ROOT}" -type f -name '*.md' \
    ! -path '*/.git/*' \
    | sed "s|${REPO_ROOT}/||" \
    | sort \
    | while read -r path; do
      printf -- '- `%s`\n' "${path}"
    done

  if [[ -f "${REPO_ROOT}/use_me_codex.md" ]]; then
    printf '\n## Related Root Markdown Files\n\n'
    printf -- '- `use_me_codex.md`\n'
  fi
} > "${OUTPUT_FILE}"

printf 'Wrote inventory: %s\n' "${OUTPUT_FILE}"
