<p align="center">
  <img src="docs/logo-text.svg" width="260" height="64" alt="Graphify"/>
</p>

# Graphify Enterprise

Graphify Enterprise is a hardened fork of graphify for organizations that need a local knowledge graph over code, documents, papers, images, and transcripts while keeping model access, network egress, and security review under enterprise control.

The tool turns a folder of source and reference material into:

- `graphify-out/graph.html` - self-contained interactive graph, no remote JavaScript CDN.
- `graphify-out/GRAPH_REPORT.md` - god nodes, communities, surprising connections, and suggested questions.
- `graphify-out/graph.json` - queryable persistent graph for assistants, CLI use, or MCP.
- `graphify-out/cache/` - SHA256 cache so re-runs only process changed files.

Use it from supported coding assistants with `/graphify` or from the CLI with `graphify`.

## What Makes This Enterprise Grade

This fork keeps the core graphify workflow and adds controls expected before a regulated enterprise rollout:

- No telemetry, analytics, run-history upload, query-answer memory, or usage-cost tracking.
- No direct public LLM API backend code or hard-coded public LLM endpoints.
- Model traffic must route through the approved assistant platform, such as Claude hosted on Amazon Bedrock through an internal gateway or GitHub Copilot Enterprise.
- Fail-closed egress policy with exact-host and wildcard-host allowlisting.
- `GRAPHIFY_DISABLE_NETWORK=1` offline mode.
- URL ingestion, repository clone, `yt-dlp`, redirects, and Neo4j push are all covered by graphify-controlled egress checks.
- Generated HTML graph output is self-contained and does not load remote visualization assets.
- Local verification commands and a security scan script are included for controlled review before internal promotion.
- Public promotional and remote-rendered documentation assets were removed from primary documentation and generated visualization paths.

This does not make any software "no risk." For broad deployment, run your own AppSec review, internal SCA/SAST, endpoint egress enforcement, DLP review, and signed artifact promotion.

## Recommended Enterprise Runtime Policy

Set these environment variables through your managed endpoint profile, shell wrapper, or internal package launcher:

```bash
export GRAPHIFY_ENTERPRISE=1
export GRAPHIFY_EGRESS_POLICY=allowlist
export GRAPHIFY_ALLOWED_HOSTS="github.company.internal,bedrock-gateway.company.internal,copilot-proxy.company.internal,neo4j.company.internal"
```

For offline-only work:

```bash
export GRAPHIFY_DISABLE_NETWORK=1
```

Do not use `GRAPHIFY_ALLOWED_HOSTS=*` in regulated environments. Prefer internal Git mirrors, internal model gateways, internal package mirrors, and approved proxy hosts.

## Security-Conscious Installation

For enterprise deployment, do not install directly from the public internet on employee machines. Mirror this repository into your internal source control system, run the verification gates, then publish a signed artifact to your internal package registry.

Recommended internal flow:

```bash
git clone https://github.com/bmjcoding/graphify-enterprise.git
cd graphify-enterprise

# Review and pin the commit you intend to promote.
git rev-parse HEAD

# Run the local verification gates.
uv run --extra sql --with pytest --with 'bandit[toml]' --with pip-audit bash scripts/security-scan.sh
uv run --with build python -m build
```

Then promote the built wheel from `dist/` only after:

- SCA/SAST findings are reviewed.
- `gitleaks` or your enterprise secrets scanner passes.
- SBOM is archived with the release.
- Build provenance is verified if required by your internal release process.
- The artifact is published to the internal package registry.

Evaluation install from the public repo:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[mcp,pdf,watch,sql]"
graphify --help
```

Pinned tool install for a controlled pilot:

```bash
uv tool install "git+https://github.com/bmjcoding/graphify-enterprise.git@<reviewed-commit-sha>"
```

## Assistant Setup

Install the graphify skill for your approved assistant:

| Platform | Install command |
|---|---|
| Claude Code | `graphify install --platform claude` |
| GitHub Copilot CLI | `graphify install --platform copilot` |
| VS Code Copilot Chat | `graphify vscode install` |
| Codex | `graphify install --platform codex` |
| OpenCode | `graphify install --platform opencode` |
| Aider | `graphify install --platform aider` |
| Cursor | `graphify cursor install` |
| Gemini CLI | `graphify install --platform gemini` |

For this enterprise fork, route assistant model calls only through approved paths:

- Claude on Amazon Bedrock behind the internal gateway.
- GitHub Copilot Enterprise through the approved tenant/proxy.

The enterprise-safe build does not include public Anthropic, OpenAI-compatible, Moonshot, or other direct public LLM API backends.

## Basic Usage

Build a graph for the current project:

```bash
/graphify .
```

Codex uses `$` instead of `/` for skill calls:

```bash
$graphify .
```

Useful CLI commands:

```bash
graphify query "show the auth flow" --graph graphify-out/graph.json
graphify path "DigestAuth" "Response"
graphify explain "SwinTransformer"
graphify watch ./src
graphify hook install
```

Enterprise-gated network features:

```bash
graphify add https://approved.example.internal/paper.pdf
graphify clone https://github.company.internal/team/repo
graphify add https://approved-video-host.example.internal/talk.mp4
graphify ./raw --neo4j-push neo4j+s://neo4j.company.internal:7687
```

Those commands fail closed when `GRAPHIFY_ENTERPRISE=1` unless the destination host is present in `GRAPHIFY_ALLOWED_HOSTS`.

## Supported Inputs

| Type | Extensions | Extraction |
|---|---|---|
| Code | `.py .ts .js .jsx .tsx .mjs .go .rs .java .c .cpp .rb .cs .kt .scala .php .swift .lua .zig .ps1 .ex .exs .m .mm .jl .vue .svelte .sql` | Local tree-sitter AST, deterministic structural edges, SQL table/view/function/foreign-key extraction |
| Docs | `.md .mdx .html .txt .rst .yaml .yml` | Assistant-mediated semantic extraction through approved model gateway |
| Office | `.docx .xlsx` | Converted locally, then assistant-mediated semantic extraction |
| PDFs | `.pdf` | Local parsing plus assistant-mediated concept extraction |
| Images | `.png .jpg .jpeg .webp .gif` | Assistant-mediated vision extraction through approved model gateway |
| Video/audio | `.mp4 .mov .mkv .webm .avi .m4v .mp3 .wav .m4a .ogg` | Local faster-whisper transcription, then semantic extraction |
| URLs | approved `http` or `https` URLs | Explicit user action only, egress-allowlisted, SSRF-guarded |

## Data Handling

Treat graph outputs as confidential source-derived work product:

- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.html`
- `graphify-out/cache/`
- `graphify-out/transcripts/`

Do not upload graph artifacts to public systems. Apply the same retention, encryption, DLP, and access-control policies that apply to the source repositories and documents being analyzed.

## Local Verification

Run these checks before promoting a reviewed commit into an internal package registry:

```bash
python3 -m compileall graphify
uv run --extra sql --with pytest pytest
uv run --extra sql --with 'bandit[toml]' bandit -r graphify -c pyproject.toml --severity-level medium --confidence-level medium
uv run --extra sql --with pip-audit pip-audit . --strict --desc off
gitleaks detect --source . --no-git --redact --verbose
git diff --check
```

## Rollout Checklist

Before broad deployment:

1. Mirror this repo into internal source control.
2. Require AppSec and platform security approval.
3. Run enterprise SCA/SAST and secrets scanning.
4. Verify signed build provenance if required by your internal release process.
5. Publish through the internal package registry.
6. Enforce endpoint or proxy egress policy matching `GRAPHIFY_ALLOWED_HOSTS`.
7. Pilot with a limited group before all-employee rollout.

See `docs/ENTERPRISE_ROLLOUT.md` for the detailed gate list.

## Relationship To Upstream

This repository is an enterprise-hardening fork of `safishamsi/graphify`. It preserves the core local knowledge-graph workflow while removing direct public LLM backends and adding enterprise controls around telemetry posture, egress, local security verification, and deployment guidance.

## License

See `LICENSE`.
