from __future__ import annotations

import pytest

from graphify.llm import BACKENDS, detect_backend, extract_files_direct


def test_direct_llm_backends_removed_from_enterprise_safe_build():
    assert BACKENDS == {}
    assert detect_backend() is None


def test_extract_files_direct_raises_enterprise_message(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("print('hello')\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Direct LLM API extraction has been removed"):
        extract_files_direct([source], root=tmp_path)
