# How To Use Codex + This Repo (End To End)

This guide is for someone starting fresh and wanting a practical path from zero to a working Codex-assisted project.

## 1. Install Codex CLI

Choose one install method:

```bash
# Option A (npm)
npm i -g @openai/codex

# Option B (Homebrew on macOS)
brew install --cask codex
```

Check install:

```bash
codex --version
```

## 2. First Run Login

Run:

```bash
codex
```

On first launch, sign in with either:
- ChatGPT account
- OpenAI API key

## 3. Download This Repository

```bash
git clone https://github.com/anujraja/Codex-Software-Developer.git
cd Codex-Software-Developer
```

## 4. Install This Repo's Codex Assets Locally

Recommended:

```bash
./scripts/install_codex_helper.sh
```

Optional:

```bash
# include reusable global guidance in ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# overwrite matching assets, with backup
./scripts/install_codex_helper.sh --force
```

Verify:

```bash
ls ~/.codex/agents
ls ~/.agents/skills
```

## 5. Test Drive In A New Project (Website Login + Local DB)

### Project idea

Build a small login app with:
- register/login/logout
- local SQLite DB
- password hashing
- session auth
- basic tests

### Steps

```bash
mkdir -p ~/codex-demos/coffee-club-login
cd ~/codex-demos/coffee-club-login
git init
codex
```

Then paste this request in Codex:

```text
Create a small but polished login web app using Node.js + Express + SQLite.
Requirements:
1) Register/login/logout flows with hashed passwords.
2) Local SQLite database stored at ./data/app.db.
3) Session-based authentication and protected dashboard route.
4) Clean minimal UI with one interesting visual style.
5) npm scripts: dev, start, test.
6) Add tests for auth flow and protected route access.
7) Add README with run/test instructions.
After code generation, run install and tests, then summarize results.
```

After Codex finishes, run:

```bash
npm run dev
```

Open `http://localhost:3000` and test register/login.

### Why this repo helps in this example

- Installed agents/skills give clearer specialization for setup, implementation, and review tasks.
- Routing docs reduce guesswork about what agent/skill to use for each stage.
- Obsidian bundle helps track what capabilities you have and how they connect.

## 6. Obsidian Vault: Which Folder To Copy

The folder meant for Obsidian is:

```text
for_obsidian/
```

### Recommended export command

From this repository root:

```bash
cd /path/to/Codex-Software-Developer
./scripts/export_obsidian_bundle.sh "/absolute/path/to/YourObsidianVault"
```

If the target folder already exists:

```bash
./scripts/export_obsidian_bundle.sh --force "/absolute/path/to/YourObsidianVault"
```

Result inside your vault:

```text
YourObsidianVault/Codex-Helper/
```

### Manual copy method (explicit cd flow)

```bash
# 1) go to your vault root
cd "/absolute/path/to/YourObsidianVault"

# 2) create a folder for this bundle
mkdir -p "Codex-Helper"
cd "Codex-Helper"

# 3) copy all markdown and related files from repo's for_obsidian folder
cp -R "/path/to/Codex-Software-Developer/for_obsidian/." .
```

Confirm markdown files copied:

```bash
find . -type f -name "*.md" | sort
```

## 7. Keep Obsidian Markdown Inventory Fresh

When you add docs in this repository, refresh the list:

```bash
cd /path/to/Codex-Software-Developer
./scripts/refresh_obsidian_inventory.sh
```

That updates:
- `for_obsidian/90_Markdown_Inventory.md`
