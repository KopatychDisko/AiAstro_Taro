"""Observability helper tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from server.observability import (
    build_langfuse_callbacks,
    flush_langfuse,
    langfuse_run_metadata,
)


def test_build_langfuse_callbacks_empty_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)

    assert build_langfuse_callbacks("user-1", "Test") == []


def test_build_langfuse_callbacks_empty_when_keys_blank(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "  ")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")

    assert build_langfuse_callbacks("user-1", "Test") == []


def test_build_langfuse_callbacks_returns_v4_handler(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    fake_handler = object()

    with patch("langfuse.langchain.CallbackHandler", return_value=fake_handler) as ctor:
        result = build_langfuse_callbacks("user-1", "Test")

    assert result == [fake_handler]
    ctor.assert_called_once_with()


def test_langfuse_run_metadata_includes_session_and_user() -> None:
    meta = langfuse_run_metadata("user-42", "Alice")
    assert meta["langfuse_session_id"] == "user-42"
    assert meta["langfuse_user_id"] == "user-42"
    assert meta["user_name"] == "Alice"
    assert "stream" in meta["langfuse_tags"]


def test_flush_langfuse_noop_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    flush_langfuse()


def test_flush_langfuse_calls_client(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    client = MagicMock()

    with patch("langfuse.get_client", return_value=client):
        flush_langfuse()

    client.flush.assert_called_once_with()
