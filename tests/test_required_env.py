"""Wave 0 tests for server.required_env fail-fast (D-09/D-11/D-12)."""

from __future__ import annotations

import pytest

import server.required_env as required_env_mod
from server.required_env import (
    REQUIRED_ENV_KEYS,
    format_missing_env_message,
    missing_required_env_keys,
    require_env_or_exit,
    require_env_or_raise,
)

_SECRET_VALUE = "super-secret-value-never-in-message"


@pytest.fixture(autouse=True)
def _disable_dotenv_load(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent repo .env from restoring keys after monkeypatch.delenv."""
    monkeypatch.setattr(required_env_mod, "_load_dotenv_from_repo", lambda: None)


def _clear_required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in REQUIRED_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)


def _set_all_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STREAM_API_KEY", _SECRET_VALUE)
    monkeypatch.setenv("OPENAI_API_KEY", _SECRET_VALUE)
    monkeypatch.setenv("ZEP_API", _SECRET_VALUE)


def test_required_env_keys_are_exactly_d09() -> None:
    assert REQUIRED_ENV_KEYS == ("STREAM_API_KEY", "OPENAI_API_KEY", "ZEP_API")
    optional = {
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "HUGGINGFACEHUB_API_TOKEN",
        "POSTGRESQL_USER",
        "POSTGRESQL_PASSWORD",
        "POSTGRESQL_HOST",
        "POSTGRESQL_PORT",
        "POSTGRESQL_DBNAME",
    }
    assert optional.isdisjoint(set(REQUIRED_ENV_KEYS))


def test_missing_required_env_keys_empty_when_all_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_all_required(monkeypatch)
    assert missing_required_env_keys() == []


@pytest.mark.parametrize("missing_key", ["STREAM_API_KEY", "OPENAI_API_KEY", "ZEP_API"])
def test_missing_required_env_keys_lists_each_absent_key(
    monkeypatch: pytest.MonkeyPatch,
    missing_key: str,
) -> None:
    _set_all_required(monkeypatch)
    monkeypatch.delenv(missing_key, raising=False)
    assert missing_required_env_keys() == [missing_key]


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_missing_required_env_keys_treats_whitespace_as_missing(
    monkeypatch: pytest.MonkeyPatch,
    blank: str,
) -> None:
    _set_all_required(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", blank)
    assert missing_required_env_keys() == ["OPENAI_API_KEY"]


def test_format_missing_env_message_lists_keys_and_env_example_hint() -> None:
    message = format_missing_env_message(["STREAM_API_KEY", "ZEP_API"])
    assert "STREAM_API_KEY" in message
    assert "ZEP_API" in message
    assert ".env.example" in message


def test_format_missing_env_message_does_not_include_secret_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STREAM_API_KEY", _SECRET_VALUE)
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("ZEP_API", _SECRET_VALUE)
    missing = missing_required_env_keys()
    message = format_missing_env_message(missing)
    assert _SECRET_VALUE not in message


def test_require_env_or_raise_ok_when_all_set(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_all_required(monkeypatch)
    require_env_or_raise()


def test_require_env_or_raise_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_required_env(monkeypatch)
    with pytest.raises(RuntimeError) as exc_info:
        require_env_or_raise()
    message = str(exc_info.value)
    assert "STREAM_API_KEY" in message
    assert ".env.example" in message


def test_require_env_or_exit_ok_when_all_set(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_all_required(monkeypatch)
    require_env_or_exit()


def test_require_env_or_exit_raises_system_exit_1(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_required_env(monkeypatch)
    with pytest.raises(SystemExit) as exc_info:
        require_env_or_exit()
    assert exc_info.value.code == 1
