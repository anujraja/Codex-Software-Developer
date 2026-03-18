# Developer Guide

Generated at: `2026-03-18T09:44:22+00:00`

## Pipeline Commands
```bash
python3 scripts/fetch_sources.py
python3 scripts/index_files.py
python3 scripts/extract_entities.py
python3 scripts/build_canonical.py
python3 scripts/build_docs.py
python3 scripts/validate_repo.py
```

## Update Workflow
1. Update `config/sources.yaml` when adding/removing source repositories.
2. Run the full pipeline in order.
3. Review `catalog/duplicates_agents.json` for merge impacts.
4. Confirm `catalog/translation_audit.csv` has no unresolved rows.
5. Run validation and commit generated outputs.

## Key Outputs
- `catalog/source_files.csv` full source file manifest
- `catalog/binary_assets.csv` binary asset index
- `catalog/canonical_entities.jsonl` canonical unified entities
- `knowledge/agents/*.toml` canonical merged agent definitions
- `knowledge/skills/*.md` canonical skill documents
- `knowledge/prompts/*.md` canonical prompt documents
