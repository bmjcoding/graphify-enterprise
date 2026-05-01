# Enterprise Rollout Checklist

This checklist is the minimum bar for deploying graphify inside a mega-bank or similarly regulated environment. It is intentionally conservative: the default enterprise posture is fail closed for outbound network access and requires independent approval before any data leaves the workstation or build environment.

## Required gates before rollout

1. Independent security review by AppSec and platform security, with sign-off outside the implementation team.
2. SCA and SAST in CI for every pull request, including dependency vulnerability review and static analysis findings triage.
3. Signed build provenance for every release artifact, with attestations verified before promotion to an internal package registry.
4. Network egress controls on endpoints, CI runners, and developer workstations.
5. Internal package distribution from an approved mirror or artifact registry.
6. Pilot deployment with endpoint telemetry from enterprise controls only, not from graphify itself.

## Enterprise runtime policy

Set these variables through the managed endpoint profile, shell wrapper, or package launcher:

```bash
export GRAPHIFY_ENTERPRISE=1
export GRAPHIFY_EGRESS_POLICY=allowlist
export GRAPHIFY_ALLOWED_HOSTS="github.company.internal,bedrock-gateway.company.internal,copilot-proxy.company.internal,neo4j.company.internal"
```

For offline-only use:

```bash
export GRAPHIFY_DISABLE_NETWORK=1
```

When `GRAPHIFY_ENTERPRISE=1` is set, graphify defaults to `allowlist` egress mode. When `GRAPHIFY_DISABLE_NETWORK=1` is set, all graphify-controlled outbound requests are blocked, including URL ingestion, repository clone, `yt-dlp` downloads, and Neo4j push.

## Approved LLM routes

graphify should be run through the approved assistant platform only:

- Claude hosted on Amazon Bedrock through the internal enterprise gateway.
- GitHub Copilot Enterprise through the bank-approved tenant and proxy path.

Direct public LLM API backends have been removed from this build. Do not add API keys for public Anthropic, OpenAI-compatible, or other public model endpoints. Any future direct gateway integration must be implemented as an internal-host-only connector, covered by egress allowlisting, SAST, SCA, threat modeling, and independent review.

## Network egress controls

Runtime egress is controlled in `graphify.security.validate_network_egress_endpoint()` and currently covers:

- `safe_fetch()` and redirects used by URL ingestion.
- `yt-dlp` URL downloads before handing control to `yt-dlp`.
- `graphify clone` GitHub repository clone URLs.
- `push_to_neo4j()` database endpoints.

Enterprise host allowlists accept exact hosts and wildcard suffixes such as `*.company.internal`. Do not use `*` in regulated deployments. Prefer internal mirrors and proxies over direct public hosts.

Recommended rollout defaults:

```bash
GRAPHIFY_ENTERPRISE=1
GRAPHIFY_EGRESS_POLICY=allowlist
GRAPHIFY_ALLOWED_HOSTS=<internal-git>,<internal-bedrock-gateway>,<copilot-enterprise-proxy>,<internal-neo4j-if-used>
```

Feature-specific approvals:

| Feature | Default enterprise posture | Required approval |
|---|---|---|
| Local code/docs graph build | Allowed | Endpoint data handling approval |
| URL ingestion | Disabled unless allowlisted | AppSec approval for domains and content handling |
| `graphify clone` | Disabled unless allowlisted | Internal Git host only, or approved proxy |
| Video URL download | Disabled unless allowlisted | AppSec approval for `yt-dlp` domains |
| Neo4j push | Disabled unless allowlisted | Internal database host and credential handling review |
| Direct public LLM APIs | Removed | Do not enable |

## Build and release provenance

Use the release provenance workflow for tag builds. It creates Python distribution artifacts, a CycloneDX SBOM, and GitHub artifact attestations. Before promotion to the internal package registry:

1. Verify the release tag is protected and signed according to bank policy.
2. Verify the GitHub build provenance attestation for every `dist/*` artifact.
3. Verify the SBOM attestation and archive the SBOM with the release.
4. Rebuild in the bank-controlled CI environment if policy requires hermetic internal builds.
5. Publish only through the approved internal package registry.

## SCA and SAST

The security workflow runs:

- CodeQL for Python semantic analysis.
- Bandit for Python SAST.
- pip-audit for Python dependency vulnerabilities.
- CycloneDX SBOM generation.

For bank rollout, mirror these controls in the internal CI system and add any required enterprise scanners. Critical findings are rollout blockers. High findings require documented risk acceptance from AppSec.

## Data handling

Treat all graphify outputs as confidential work product:

- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.html`
- `graphify-out/cache/`
- `graphify-out/transcripts/`

Do not upload generated graph artifacts to public services. Apply retention, encryption, and DLP rules consistent with source-code handling.

## Pull request controls

Before merging enterprise rollout changes:

- Require CODEOWNERS review from AppSec and platform security teams.
- Require passing CI, security workflow, and provenance dry run where applicable.
- Require explicit review of network egress changes.
- Require dependency lockfile or internal artifact mirror review.
- Require a release note describing any new outbound connection or third-party dependency.

## Director-level sign-off position

This repository can be hardened for enterprise use, but it should not be represented as "no risk." A mega-bank rollout should be approved only after the controls above are implemented in the bank environment, verified independently, and monitored through existing enterprise endpoint and network controls.
