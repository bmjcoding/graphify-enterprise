"""Compatibility shims for removed direct LLM API extraction.

graphify's supported extraction path is the managed assistant platform that
invokes the packaged skill. Enterprise deployments must route model traffic
through their approved assistant gateway, such as Claude on Amazon Bedrock
behind an internal gateway or GitHub Copilot Enterprise.

This module intentionally contains no hard-coded public model endpoints and no
SDK imports that could send source material to an external LLM API.
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


BACKENDS: dict[str, dict] = {}


def _direct_llm_removed() -> RuntimeError:
    return RuntimeError(
        "Direct LLM API extraction has been removed from this enterprise-safe "
        "build. Use the packaged graphify skill through an approved managed "
        "assistant platform such as an internal Amazon Bedrock Claude gateway "
        "or GitHub Copilot Enterprise."
    )


def extract_files_direct(
    files: list[Path],
    backend: str = "",
    api_key: str | None = None,
    model: str | None = None,
    root: Path = Path("."),
) -> dict:
    """Direct public LLM API extraction is not available."""
    raise _direct_llm_removed()


def extract_corpus_parallel(
    files: list[Path],
    backend: str = "",
    api_key: str | None = None,
    model: str | None = None,
    root: Path = Path("."),
    chunk_size: int = 20,
    on_chunk_done: Callable | None = None,
) -> dict:
    """Direct public LLM API extraction is not available."""
    raise _direct_llm_removed()


def detect_backend() -> str | None:
    """No direct LLM backend is auto-detected in enterprise-safe builds."""
    return None
