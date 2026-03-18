#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "sources.yaml"
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SOURCES_DIR = DATA_DIR / "sources"
CATALOG_DIR = REPO_ROOT / "catalog"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"
DOCS_DIR = REPO_ROOT / "docs"

TEXT_EXTS = {
    "md",
    "toml",
    "yaml",
    "yml",
    "json",
    "py",
    "js",
    "sh",
    "txt",
    "html",
    "css",
    "xml",
    "env",
    "example",
    "gitignore",
    "npmignore",
    "swift",
    "bat",
    "ps1",
    "lock",
    "",
}

BINARY_EXTS = {
    "ttf",
    "otf",
    "woff",
    "woff2",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "svg",
    "pdf",
    "ico",
    "webp",
    "zip",
    "gz",
    "tar",
    "7z",
    "dmg",
    "exe",
    "dll",
    "so",
    "bin",
    "class",
    "jar",
}

LANGUAGE_KEYWORDS = {
    "python": ["python", "pyproject", "pytest", "django", "fastapi", "flask"],
    "typescript": ["typescript", "tsconfig", "tsx", ".ts"],
    "javascript": ["javascript", "node", "npm", ".js"],
    "go": ["golang", " go ", "go.mod"],
    "rust": ["rust", "cargo", ".rs"],
    "java": ["java", "spring", ".java"],
    "kotlin": ["kotlin", ".kt", "ktor"],
    "swift": ["swift", "swiftui", "xcode", "ios", "macos"],
    "ruby": ["ruby", "rails", "gemfile"],
    "php": ["php", "laravel", "composer"],
    "csharp": ["c#", "csharp", "dotnet", ".net", "asp.net"],
    "cpp": ["c++", "cpp", ".hpp", ".cpp"],
    "c": ["embedded", "firmware", ".c", ".h"],
    "elixir": ["elixir", "phoenix", "otp"],
    "clojure": ["clojure"],
    "scala": ["scala"],
    "sql": ["sql", "postgres", "mysql", "sqlite", "query"],
    "react": ["react", "jsx"],
    "vue": ["vue", "nuxt"],
    "angular": ["angular"],
    "powershell": ["powershell", "pwsh"],
}

SYSTEM_KEYWORDS = {
    "aws": ["aws", "eks", "lambda", "cloudwatch"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker", "container"],
    "kubernetes": ["kubernetes", "k8s", "helm"],
    "terraform": ["terraform", "terragrunt"],
    "github": ["github", "actions", "gh "],
    "git": ["git", "branch", "merge", "rebase"],
    "mcp": ["mcp", "model context protocol"],
    "notion": ["notion"],
    "slack": ["slack"],
    "linear": ["linear"],
    "postgres": ["postgres", "postgresql"],
    "redis": ["redis"],
    "linux": ["linux"],
    "windows": ["windows", "active directory", "powershell"],
    "ios": ["ios", "swiftui", "xcode"],
}

ROLE_KEYWORDS = [
    "developer",
    "engineer",
    "architect",
    "reviewer",
    "auditor",
    "manager",
    "analyst",
    "designer",
    "specialist",
    "expert",
    "coordinator",
    "tester",
    "writer",
    "administrator",
    "admin",
    "orchestrator",
]

ENGLISH_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "you",
    "your",
    "use",
    "this",
    "that",
    "from",
    "into",
    "build",
    "review",
    "when",
    "what",
    "how",
    "task",
    "code",
    "data",
    "system",
    "agent",
}

FOREIGN_HINTS = {
    "vous",
    "votre",
    "avec",
    "pour",
    "dans",
    "donnees",
    "données",
    "implémentation",
    "et",
    "les",
    "des",
    "une",
    "est",
    "sont",
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def parse_key_value(raw: str) -> tuple[str, str]:
    key, value = raw.split(":", 1)
    return key.strip(), value.strip().strip('"').strip("'")


def load_sources(path: Path = CONFIG_PATH) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    sources: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "sources:":
            continue

        if stripped.startswith("- "):
            if current:
                sources.append(current)
            current = {}
            payload = stripped[2:].strip()
            if payload and ":" in payload:
                k, v = parse_key_value(payload)
                current[k] = v
            continue

        if current is None:
            continue

        if ":" in stripped:
            k, v = parse_key_value(stripped)
            current[k] = v

    if current:
        sources.append(current)

    required = {"owner", "repo", "branch"}
    for src in sources:
        missing = required - set(src)
        if missing:
            raise ValueError(f"Missing fields in source definition {src}: {sorted(missing)}")

    return sources


def source_repo_id(source: dict[str, str]) -> str:
    return f"{source['owner']}/{source['repo']}"


def source_slug(source: dict[str, str]) -> str:
    return f"{source['owner']}__{source['repo']}__{source['branch']}"


def codeload_url(source: dict[str, str]) -> str:
    return (
        f"https://codeload.github.com/{source['owner']}/{source['repo']}"
        f"/tar.gz/refs/heads/{source['branch']}"
    )


def raw_file_url(source: dict[str, str], path: str) -> str:
    encoded_path = urllib.parse.quote(path)
    return (
        f"https://raw.githubusercontent.com/{source['owner']}/{source['repo']}"
        f"/{source['branch']}/{encoded_path}"
    )


def sha256_bytes(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 128)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def file_ext(path: str) -> str:
    name = Path(path).name
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[1].lower()


def classify_bytes(path: str, data: bytes) -> str:
    ext = file_ext(path)
    if ext in BINARY_EXTS:
        return "binary"
    if ext in TEXT_EXTS:
        return "text"
    if b"\x00" in data[:8192]:
        return "binary"
    try:
        data[:8192].decode("utf-8")
    except UnicodeDecodeError:
        return "binary"
    return "text"


def guess_asset_purpose(path: str) -> str:
    ext = file_ext(path)
    if ext in {"ttf", "otf", "woff", "woff2"}:
        return "font asset"
    if ext in {"png", "jpg", "jpeg", "gif", "svg", "ico", "webp"}:
        return "image asset"
    if ext == "pdf":
        return "reference document"
    if ext in {"zip", "gz", "tar", "7z"}:
        return "archive"
    return "binary asset"


def normalize_name(name: str) -> str:
    lowered = name.strip().lower()
    lowered = lowered.replace("_", "-").replace(" ", "-")
    lowered = re.sub(r"[^a-z0-9\-]+", "-", lowered)
    lowered = re.sub(r"\-+", "-", lowered).strip("-")
    return lowered or "unnamed"


def slugify(value: str) -> str:
    return normalize_name(value)


def short_summary(text: str, limit: int = 220) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def extract_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---"):
        return {}, markdown

    parts = markdown.split("---", 2)
    if len(parts) < 3:
        return {}, markdown

    raw_fm = parts[1]
    body = parts[2].lstrip("\n")
    fm: dict[str, str] = {}

    for line in raw_fm.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip().strip('"')

    return fm, body


def parse_toml_key(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*\"([^\"]*)\"", text)
    return match.group(1).strip() if match else ""


def parse_toml_multiline(text: str, key: str) -> str:
    match = re.search(
        rf"{re.escape(key)}\s*=\s*\"\"\"(.*?)\"\"\"",
        text,
        flags=re.S,
    )
    return match.group(1).strip() if match else ""


def parse_toml_array(text: str, key: str) -> list[str]:
    match = re.search(rf"(?s){re.escape(key)}\s*=\s*\[(.*?)\]", text)
    if not match:
        return []
    raw = match.group(1)
    values = re.findall(r'"([^\"]+)"', raw)
    return [item.strip() for item in values if item.strip()]


def detect_keywords(blob: str, mapping: dict[str, list[str]]) -> list[str]:
    hay = f" {blob.lower()} "
    found: list[str] = []
    for label, patterns in mapping.items():
        for pattern in patterns:
            token = f" {pattern.lower()} "
            if token.strip() in {".ts", ".js", ".rs", ".java", ".kt", ".cpp", ".hpp", ".c", ".h", ".net"}:
                if token.strip() in hay:
                    found.append(label)
                    break
                continue
            if token in hay:
                found.append(label)
                break
    return sorted(set(found))


def detect_languages(path: str, text: str) -> list[str]:
    blob = f"{path}\n{text[:12000]}"
    return detect_keywords(blob, LANGUAGE_KEYWORDS)


def detect_systems(path: str, text: str) -> list[str]:
    blob = f"{path}\n{text[:12000]}"
    return detect_keywords(blob, SYSTEM_KEYWORDS)


def detect_roles(name: str, text: str) -> list[str]:
    blob = f"{name} {text[:2000]}".lower()
    found = [role for role in ROLE_KEYWORDS if role in blob]
    return sorted(set(found))


def detect_jobs(path: str) -> list[str]:
    parts = [p for p in path.split("/") if p]
    if not parts:
        return []
    jobs = [parts[0]]
    if len(parts) > 1:
        jobs.append(parts[1])
    return sorted(set(normalize_name(j) for j in jobs))


def extract_steps(text: str, limit: int = 20) -> list[str]:
    steps: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:\d+[\.)]|[-*])\s+(.+)", line)
        if not match:
            continue
        step = " ".join(match.group(1).split())
        if step and step not in steps:
            steps.append(step)
        if len(steps) >= limit:
            break
    return steps


def is_probably_english(text: str) -> bool:
    sample = text[:12000]
    tokens = [t.lower() for t in re.findall(r"[A-Za-zÀ-ÿ']+", sample)]
    if not tokens:
        return True

    english_hits = sum(1 for t in tokens if t in ENGLISH_WORDS)
    foreign_hits = sum(1 for t in tokens if t in FOREIGN_HINTS)
    accented_hits = sum(1 for t in tokens if any(ord(ch) > 127 for ch in t))

    if foreign_hits >= english_hits + 4:
        return False
    if accented_hits >= max(8, len(tokens) // 8) and english_hits < 4:
        return False
    return True


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def markdown_escape_pipe(value: str) -> str:
    return value.replace("|", "\\|")
