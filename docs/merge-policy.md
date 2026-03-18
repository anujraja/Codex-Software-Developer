# Merge Policy

Generated at: `2026-03-18T08:06:29+00:00`

## Canonicalization Rules
1. Source inputs are parsed into normalized entity contracts in `catalog/*.jsonl`.
2. For duplicate agent names, one canonical file is generated per normalized name.
3. Canonical agent files preserve explicit provenance comments for every source reference.
4. Skills and prompts are generated as canonical Markdown knowledge entries with provenance sections.
5. Binary files are not copied; they remain indexed by URL and hash in `catalog/binary_assets.csv`.

## Translation Rules
1. Canonical outputs must be English-first.
2. Non-English text is auto-normalized to English during canonical build.
3. Translation outcomes are tracked in `catalog/translation_audit.csv`.

## Determinism
- Sorting is stable for all entity lists and output paths.
- Regeneration may change timestamps, but logical content and counts remain stable.
