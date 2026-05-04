---
type: research
status: completed
slug: skills-skill-container-capabilities
summary: "U1: git is NOT confirmed pre-installed in the claude.ai container; use GitHub REST API via Python requests instead. U2: filesystem does NOT persist between conversations; every session must assume a fresh container."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: skills-skill-container-capabilities
research_friction_level: FL1
---

# Research Output: claude.ai Container Capabilities for skills-skill Bootstrap

## Executive Summary

The `skills-skill` architecture spec (`research/skills-skill-architecture/output/SPEC.md`) contained two CRITICAL UNCERTAIN markers blocking implementation:

- **U1**: Whether `git` is available in the claude.ai session container.
- **U2**: Whether the claude.ai container filesystem persists between sessions.

This research resolves both. Key findings:

| Marker | Finding | Confidence |
|---|---|---|
| U1: git binary | NOT confirmed pre-installed. Official pre-installed utility list omits git. | (a) official list + (d) inference |
| U1: bash execution | CONFIRMED. Claude uses `bash_code_execution` sub-tool; SKILL.md instructs Claude, not a shell. | (a) Anthropic-official |
| U1: network (Free/Pro/Max) | CONFIRMED available to GitHub. Best-practices page states Skills "can pull from GitHub repositories." | (a) Anthropic-official |
| U1: network (Team/Enterprise) | Disabled by default. REST API approach also fails. Must use Files API offline fallback. | (a) Anthropic-official |
| U2: per-session persistence | NOT guaranteed. No documented mechanism for auto-reuse between conversations in the web UI. | (d) inference + GitHub issue evidence |
| U2: container lifetime | Up to 30 days, but reuse requires explicit container ID (API only, not exposed in web UI). | (a) Anthropic-official |

**Architectural impact**: The git-based B1–B5 bootstrap sequence must be replaced with a GitHub REST API sequence for claude.ai. Claude Code is unaffected (git is available on the host). Every session must be treated as a fresh start.

---

## 1. How Skills Execute in claude.ai

SKILL.md is a markdown document injected into Claude's context window, not a shell script. Claude then uses its `bash_code_execution` sub-tool to run any commands that the SKILL.md body instructs it to run. This is confirmed by Anthropic's engineering blog:

> "When a Skill is triggered, Claude uses bash to read SKILL.md from the filesystem, bringing its instructions into the context window… When instructions mention executable scripts, Claude runs them via bash and receives only the output."
>
> — Anthropic Engineering Blog, *Equipping agents for the real world with Agent Skills*

This means: a SKILL.md body can include instructions like "run `git clone …`" and Claude will attempt to execute that via bash — subject to whether git is present in the container.

---

## 2. U1 — git Availability

### 2.1 Pre-Installed Environment

The code execution tool documentation lists the complete pre-installed utility set:

> "Utilities: tqdm, python-dateutil, pytz, joblib, unzip, unrar, 7zip, bc, rg (ripgrep), fd, sqlite"

**Git is not listed.** The runtime is: Python 3.11.12, Linux x86_64, with the above utilities plus a standard data science Python library stack.

### 2.2 Network Access by Plan

| Surface | Network Access |
|---|---|
| claude.ai (Free/Pro/Max) | Varying — full or partial depending on user/admin settings; GitHub is reachable on Free/Pro/Max |
| claude.ai (Team/Enterprise) | Disabled by default |
| Claude API | Completely disabled |
| Claude Code | Full (same as host OS) |

Source: Agent Skills overview page, "Runtime environment constraints" section.

The best-practices page states explicitly: "claude.ai: Can install packages from npm and PyPI and **pull from GitHub repositories**."

### 2.3 Interpretation

"Pull from GitHub repositories" likely means one or more of:
- `pip install git+https://github.com/…` (if git is present)
- `pip install https://github.com/…/archive/main.zip` (HTTP-only, no git needed)
- GitHub REST API calls via Python `requests`

It does **not** confirm git is a pre-installed binary. The conservative and correct architectural decision is: **assume git is absent; use the GitHub REST API as the primary mechanism**.

### 2.4 RFC-2119 Patch for UNCERTAIN(U1)

Replace the `> **UNCERTAIN (U1)**` block in `research/skills-skill-architecture/output/SPEC.md` §2.2 with:

---

> **RESOLVED (U1)**: The claude.ai code execution container provides bash command execution capability; Claude MUST use the `bash_code_execution` sub-tool to run shell commands. Git is NOT confirmed as a pre-installed binary in the claude.ai code execution environment; the official pre-installed utility list (unzip, unrar, 7zip, bc, rg, fd, sqlite) does not include git. Skill implementations targeting claude.ai MUST NOT assume git is available. When network access is enabled (the default for Free/Pro/Max plans), the GitHub REST API is available and MUST be used as the primary mechanism for fetching content from public GitHub repositories, using Python's `requests` library or `urllib.request`. Skills MAY attempt a `git` command as a first-try with graceful fallback to the REST API. The Claude API code execution environment has no network access; git clone MUST NOT be used there. Claude Code has full network access and git IS available via the user's host system.

---

---

## 3. U2 — Filesystem Persistence Between Sessions

### 3.1 Container Lifetime

From the code execution tool documentation:

> "Containers expire 30 days after creation."
> "You can reuse an existing container across multiple API requests by providing the container ID from a previous response. This allows you to maintain created files between requests."

### 3.2 Web UI Behaviour

The container ID mechanism is an API-level feature. The claude.ai web interface does not expose container ID selection to the user. There is no documented mechanism for automatic container reuse between independent conversations in the web UI. A GitHub issue requesting shared persistent storage between claude.ai and Claude Code (issue #28307) was closed as a duplicate — indicating persistent cross-session storage is a requested feature, not a current one.

**Practical conclusion**: Each new claude.ai conversation SHOULD be treated as starting with a fresh container.

### 3.3 Container Specs

| Resource | Limit |
|---|---|
| RAM | 5 GiB |
| Workspace storage | 5 GiB |
| CPU | 1 core |
| Data retention | Up to 30 days |

### 3.4 RFC-2119 Patch for UNCERTAIN(U2)

Replace the `> **UNCERTAIN (U2)**` block in `research/skills-skill-architecture/output/SPEC.md` §2.2 with:

---

> **RESOLVED (U2)**: The claude.ai code execution container does NOT guarantee automatic filesystem persistence between independent web conversations. While a container survives for up to 30 days after creation and can be explicitly reused via container ID in API calls, the claude.ai web interface does not expose container ID management to users, and each new conversation MUST be treated as starting with a fresh container. The git-fetch pull-if-exists optimisation (Step B2 in the architecture) MUST NOT be relied upon in the claude.ai web interface. All bootstrap sequences MUST assume no prior local clone exists and MUST re-fetch required files on each invocation. Container workspace provides 5 GiB storage and 5 GiB RAM within the session.

---

---

## 4. Alternative Bootstrap Mechanisms (U1 = git absent)

Ranked from most practical to least for the claude.ai Free/Pro/Max surface:

### 4.1 GitHub REST API via Python requests (RECOMMENDED)

```python
import requests, base64

def fetch_skill(owner, repo, path, branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    r = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    r.raise_for_status()
    return base64.b64decode(r.json()["content"]).decode()
```

For full directory tree: `GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`

| Factor | Assessment |
|---|---|
| Availability | Python pre-installed; `requests` almost certainly available |
| Auth | None for public repos |
| Rate limit | 60 req/hr unauthenticated; 5000/hr with token |
| Latency | ~100–300ms per file fetch |
| Suitability | High — granular, no binary dependency |

### 4.2 GitHub Archive ZIP Download

`https://github.com/{owner}/{repo}/archive/refs/heads/main.zip`

Fetch with `urllib.request.urlretrieve()` or `requests`, extract with `zipfile` (stdlib) or pre-installed `unzip`.

| Factor | Assessment |
|---|---|
| Availability | No binary dependency; stdlib only |
| Latency | Higher (downloads entire repo) |
| Suitability | Medium — simpler code, higher latency/data cost |

### 4.3 pip install from GitHub archive

`pip install https://github.com/{owner}/{repo}/archive/main.zip`

Only viable if the skills repo is structured as a Python package. Not applicable to this repository's current layout.

### 4.4 GitHub MCP Server (NOT default)

The GitHub MCP server is NOT registered by default in claude.ai sessions. Requires manual setup at claude.ai/customize/connectors. Cannot be relied upon as a universal bootstrap mechanism.

### 4.5 Anthropic Files API (Offline fallback for Team/Enterprise)

Pre-upload skill body files via the Files API; reference by file ID in SKILL.md. No network access required during the session. Required for Team/Enterprise plans where network is disabled by default.

---

## 5. Revised Bootstrap Sequence for claude.ai

Replace Steps B1–B3 from the architecture spec with the following for the claude.ai surface:

**Step B1-rest** — Fetch the skill index using the GitHub REST API:

```python
import requests, base64, json

REPO = "netzkontrast/agency"
BRANCH = "main"

def fetch_file(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    r = requests.get(url)
    r.raise_for_status()
    return base64.b64decode(r.json()["content"]).decode()

# Fetch the skills index
index = fetch_file("skills/index.json")  # or equivalent
```

**Step B2-rest** — Parse the index to identify the requested skill body path.

**Step B3-rest** — Fetch the skill body file content.

**Step B4** — Inject the skill body into the current session context and cede control. (Unchanged.)

**Step B5** — Surface a staleness notice if the API returns a `Last-Modified` header older than N days.

The git-based B1–B3 sequence remains valid for **Claude Code** deployments (git is available on the host).

---

## 6. Open Questions Surfaced

The following unresolved questions are being filed as follow-up prompts in `/prompts/`:

1. **`skills-skill-enterprise-offline`** — For Team/Enterprise plans with network disabled, the REST API approach fails entirely. A Files API pre-upload workflow must be specified. What is the maintenance burden and automation story for keeping pre-uploaded files current?

2. **`claude-ai-container-git-verification`** — The U1 finding (git absent) is rated (d) inference based on omission from the official list. A definitive yes/no requires empirical testing: execute `which git && git --version` in a claude.ai code execution session. This should be done once by any user with claude.ai Pro/Max access.
