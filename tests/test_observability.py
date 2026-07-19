"""Observability helper tests."""

from __future__ import annotations

import os

from server.observability import build_langfuse_callbacks


def test_build_langfuse_callbacks_empty_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)

    assert build_langfuse_callbacks("user-1", "Test") == []
