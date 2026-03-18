#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from common import (
    CATALOG_DIR,
    SOURCES_DIR,
    detect_jobs,
    detect_languages,
    detect_roles,
    detect_systems,
    ensure_dir,
    extract_frontmatter,
    extract_steps,
    file_ext,
    is_probably_english,
    normalize_name,
    parse_toml_array,
    parse_toml_key,
    parse_toml_multiline,
    raw_file_url,
    read_jsonl,
    short_summary,
    slugify,
    source_repo_id,
    source_slug,
    utc_now_iso,
    write_json,
    write_jsonl,
)


def source_ref(source: dict[str, str], rel_path: str) -> dict[str, str]:
    return {
        "source_repo": source_repo_id(source),
        "source_branch": source["branch"],
        "source_path": rel_path,
        "raw_url": raw_file_url(source, rel_path),
    }


def make_entity(
    *,
    entity_type: str,
    name: str,
    summary: str,
    instructions: str,
    tags: list[str],
    languages: list[str],
    systems: list[str],
    jobs: list[str],
    roles: list[str],
    steps: list[str],
    refs: list[dict[str, str]],
    extra: dict[str, str] | None = None,
) -> dict:
    normalized_name = normalize_name(name)
    record = {
        "id": f"{entity_type}--{normalized_name}--{slugify(refs[0]['source_repo'])}",
        "name": normalized_name,
        "entity_type": entity_type,
        "summary": summary.strip(),
        "instructions": instructions.strip(),
        "tags": sorted(set(t for t in tags if t)),
        "languages": sorted(set(languages)),
        "systems": sorted(set(systems)),
        "jobs": sorted(set(jobs)),
        "roles": sorted(set(roles)),
        "steps": steps,
        "source_refs": refs,
    }
    record["translation_status"] = "english" if is_probably_english(summary + "\n" + instructions) else "needs_translation"
    if extra:
        record.update(extra)
    return record


def parse_agent(source: dict[str, str], rel_path: str, text: str) -> dict:
    stem = Path(rel_path).stem
    name = parse_toml_key(text, "name") or stem
    description = parse_toml_key(text, "description")
    instructions = parse_toml_multiline(text, "developer_instructions")
    model = parse_toml_key(text, "model")
    reasoning = parse_toml_key(text, "model_reasoning_effort")
    sandbox_mode = parse_toml_key(text, "sandbox_mode")
    tags = parse_toml_array(text, "tags")

    if not description:
        description = short_summary(instructions or f"Canonical definition for {name}", 240)

    languages = detect_languages(rel_path, text)
    systems = detect_systems(rel_path, text)
    jobs = detect_jobs(rel_path)
    roles = detect_roles(name, f"{description}\n{instructions}")
    steps = extract_steps(instructions)

    tags.extend(jobs)

    return make_entity(
        entity_type="agent",
        name=name,
        summary=description,
        instructions=instructions or description,
        tags=tags,
        languages=languages,
        systems=systems,
        jobs=jobs,
        roles=roles,
        steps=steps,
        refs=[source_ref(source, rel_path)],
        extra={
            "model": model,
            "model_reasoning_effort": reasoning,
            "sandbox_mode": sandbox_mode,
            "category": rel_path.split("/")[0] if "/" in rel_path else "root",
        },
    )


def parse_markdown_agent(source: dict[str, str], rel_path: str, text: str) -> dict:
    stem = Path(rel_path).stem
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    heading = ""
    for line in lines:
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            break

    name = heading or stem
    summary = ""
    for line in lines:
        if line.startswith("#"):
            continue
        summary = line
        break

    if not summary:
        summary = short_summary(text, 240)

    jobs = detect_jobs(rel_path)
    tags = jobs + [Path(rel_path).parent.name, "markdown-agent"]

    return make_entity(
        entity_type="agent",
        name=name,
        summary=summary,
        instructions=text.strip() or summary,
        tags=tags,
        languages=detect_languages(rel_path, text),
        systems=detect_systems(rel_path, text),
        jobs=jobs,
        roles=detect_roles(name, text),
        steps=extract_steps(text),
        refs=[source_ref(source, rel_path)],
        extra={
            "model": "",
            "model_reasoning_effort": "",
            "sandbox_mode": "",
            "category": rel_path.split("/")[0] if "/" in rel_path else "root",
        },
    )


def parse_skill(source: dict[str, str], rel_path: str, text: str) -> dict:
    frontmatter, body = extract_frontmatter(text)
    folder_name = Path(rel_path).parent.name
    name = frontmatter.get("name", folder_name)
    description = frontmatter.get("description", "").strip()

    if not description:
        description = short_summary(body, 240)

    jobs = detect_jobs(rel_path)
    tags = jobs + [folder_name, "skill"]

    return make_entity(
        entity_type="skill",
        name=name,
        summary=description,
        instructions=body.strip() or description,
        tags=tags,
        languages=detect_languages(rel_path, text),
        systems=detect_systems(rel_path, text),
        jobs=jobs,
        roles=detect_roles(name, body),
        steps=extract_steps(body),
        refs=[source_ref(source, rel_path)],
        extra={
            "category": rel_path.split("/")[0] if "/" in rel_path else "root",
        },
    )


def parse_prompt_file(source: dict[str, str], rel_path: str, text: str) -> dict:
    name = Path(rel_path).stem
    summary = short_summary(text, 220)
    jobs = detect_jobs(rel_path)

    return make_entity(
        entity_type="prompt",
        name=name,
        summary=summary,
        instructions=text,
        tags=jobs + ["prompt"],
        languages=detect_languages(rel_path, text),
        systems=detect_systems(rel_path, text),
        jobs=jobs,
        roles=detect_roles(name, text),
        steps=extract_steps(text),
        refs=[source_ref(source, rel_path)],
        extra={"category": rel_path.split("/")[0] if "/" in rel_path else "root"},
    )


def parse_openai_yaml_prompt(source: dict[str, str], rel_path: str, text: str) -> dict:
    display_name = ""
    short_description = ""
    default_prompt = ""

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("display_name:"):
            display_name = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("short_description:"):
            short_description = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("default_prompt:"):
            default_prompt = stripped.split(":", 1)[1].strip().strip('"')

    name = display_name or Path(rel_path).parent.parent.name
    summary = short_description or short_summary(default_prompt, 220)
    instructions = default_prompt or summary
    jobs = detect_jobs(rel_path)

    return make_entity(
        entity_type="prompt",
        name=f"{name}-default-prompt",
        summary=summary,
        instructions=instructions,
        tags=jobs + ["default-prompt", "openai-yaml"],
        languages=detect_languages(rel_path, text),
        systems=detect_systems(rel_path, text),
        jobs=jobs,
        roles=detect_roles(name, text),
        steps=extract_steps(instructions),
        refs=[source_ref(source, rel_path)],
        extra={"category": rel_path.split("/")[0] if "/" in rel_path else "root"},
    )


def is_agent_path(rel_path: str) -> bool:
    lower = rel_path.lower()
    return lower.endswith(".toml") and (lower.startswith("agents/") or lower.startswith("categories/"))


def is_markdown_agent_path(source: dict[str, str], rel_path: str) -> bool:
    lower = rel_path.lower()
    if not lower.endswith(".md"):
        return False
    if lower.endswith("skill.md"):
        return False

    repo_id = source_repo_id(source).lower()
    if repo_id != "msitarzewski/agency-agents":
        return False

    name = Path(rel_path).name.lower()
    if name in {"readme.md", "executive-brief.md", "quickstart.md"}:
        return False

    top = rel_path.split("/", 1)[0].lower()
    excluded_top = {"examples", "strategy", "integrations", "scripts"}
    if top in excluded_top:
        return False

    return True


def is_skill_path(rel_path: str) -> bool:
    return rel_path.lower().endswith("skill.md")


def is_prompt_path(rel_path: str) -> bool:
    lower = rel_path.lower()
    ext = file_ext(lower)
    if lower.endswith("agents/openai.yaml"):
        return True
    if ext not in {"md", "txt", "toml", "yaml", "yml"}:
        return False
    return "prompt" in lower or lower.startswith("prompts/")


def build_taxonomy(agents: list[dict], skills: list[dict], prompts: list[dict]) -> dict:
    counters = {
        "roles": Counter(),
        "jobs": Counter(),
        "languages": Counter(),
        "systems": Counter(),
        "categories": Counter(),
    }

    for record in [*agents, *skills, *prompts]:
        for role in record.get("roles", []):
            counters["roles"][role] += 1
        for job in record.get("jobs", []):
            counters["jobs"][job] += 1
        for language in record.get("languages", []):
            counters["languages"][language] += 1
        for system in record.get("systems", []):
            counters["systems"][system] += 1
        category = record.get("category", "root")
        counters["categories"][category] += 1

    payload = {
        "generated_at_utc": utc_now_iso(),
        "counts": {
            "agents": len(agents),
            "skills": len(skills),
            "prompts": len(prompts),
            "total_entities": len(agents) + len(skills) + len(prompts),
        },
        "roles": [{"name": k, "count": v} for k, v in counters["roles"].most_common()],
        "jobs": [{"name": k, "count": v} for k, v in counters["jobs"].most_common()],
        "languages": [{"name": k, "count": v} for k, v in counters["languages"].most_common()],
        "systems": [{"name": k, "count": v} for k, v in counters["systems"].most_common()],
        "categories": [{"name": k, "count": v} for k, v in counters["categories"].most_common()],
    }
    return payload


def build_duplicate_agents(agents: list[dict]) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for agent in agents:
        groups[agent["name"]].append(agent)

    duplicate_groups: list[dict] = []
    for name, items in sorted(groups.items()):
        repos = sorted({ref["source_repo"] for item in items for ref in item["source_refs"]})
        if len(repos) <= 1:
            continue

        duplicate_groups.append(
            {
                "name": name,
                "repo_count": len(repos),
                "source_repos": repos,
                "entries": [
                    {
                        "id": item["id"],
                        "model": item.get("model", ""),
                        "model_reasoning_effort": item.get("model_reasoning_effort", ""),
                        "sandbox_mode": item.get("sandbox_mode", ""),
                        "source_refs": item["source_refs"],
                    }
                    for item in sorted(
                        items,
                        key=lambda x: (x["source_refs"][0]["source_repo"], x["source_refs"][0]["source_path"]),
                    )
                ],
            }
        )

    return {
        "generated_at_utc": utc_now_iso(),
        "total_duplicate_names": len(duplicate_groups),
        "duplicate_groups": duplicate_groups,
    }


def run() -> None:
    ensure_dir(CATALOG_DIR)

    agents: list[dict] = []
    skills: list[dict] = []
    prompts: list[dict] = []

    from common import load_sources  # local import to avoid cycle in static checkers

    for source in load_sources():
        slug = source_slug(source)
        root = SOURCES_DIR / slug
        if not root.exists():
            raise FileNotFoundError(f"Missing source extract: {root}. Run scripts/fetch_sources.py first.")

        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel_path = path.relative_to(root).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")

            if is_agent_path(rel_path):
                agents.append(parse_agent(source, rel_path, text))
            if is_markdown_agent_path(source, rel_path):
                agents.append(parse_markdown_agent(source, rel_path, text))
            if is_skill_path(rel_path):
                skills.append(parse_skill(source, rel_path, text))
            if is_prompt_path(rel_path):
                if rel_path.lower().endswith("agents/openai.yaml"):
                    prompts.append(parse_openai_yaml_prompt(source, rel_path, text))
                else:
                    prompts.append(parse_prompt_file(source, rel_path, text))

    agents.sort(key=lambda r: (r["name"], r["source_refs"][0]["source_repo"], r["source_refs"][0]["source_path"]))
    skills.sort(key=lambda r: (r["name"], r["source_refs"][0]["source_repo"], r["source_refs"][0]["source_path"]))
    prompts.sort(key=lambda r: (r["name"], r["source_refs"][0]["source_repo"], r["source_refs"][0]["source_path"]))

    write_jsonl(CATALOG_DIR / "agents.jsonl", agents)
    write_jsonl(CATALOG_DIR / "skills.jsonl", skills)
    write_jsonl(CATALOG_DIR / "prompts.jsonl", prompts)

    write_json(CATALOG_DIR / "taxonomy.json", build_taxonomy(agents, skills, prompts))
    write_json(CATALOG_DIR / "duplicates_agents.json", build_duplicate_agents(agents))

    print(f"Extracted agents: {len(agents)}")
    print(f"Extracted skills: {len(skills)}")
    print(f"Extracted prompts: {len(prompts)}")


if __name__ == "__main__":
    run()
