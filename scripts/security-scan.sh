#!/usr/bin/env bash
set -euo pipefail

python -m compileall graphify
python -m pytest tests/ -q --tb=short
python -m bandit -r graphify -c pyproject.toml --severity-level medium --confidence-level medium
python -m pip_audit . --strict --desc off

matches="$(
  rg -n \
    "api\.anthropic\.com|api\.moonshot\.ai|MOONSHOT|ANTHROPIC_API_KEY|from openai|import openai|from anthropic|import anthropic|resp\.usage|input_tokens|output_tokens|save-result|cost\.json|graphify-out/memory|unpkg|vis-network" \
    graphify tests README.md SECURITY.md docs pyproject.toml .github \
    || true
)"

if [[ -n "$matches" ]]; then
    printf '%s\n' "$matches"
    echo "security-scan: prohibited endpoint, tracking, or remote asset marker found" >&2
    exit 1
fi

echo "security-scan: passed"
