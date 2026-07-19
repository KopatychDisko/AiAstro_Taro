"""Shared required-env fail-fast for setup CLI and FastAPI lifespan (D-09/D-11/D-12)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REQUIRED_ENV_KEYS: tuple[str, ...] = (
    "STREAM_API_KEY",
    "OPENAI_API_KEY",
    "ZEP_API",
)

ENV_HINT = "Copy .env.example to .env and fill the missing keys."


def _load_dotenv_from_repo() -> None:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        env_file = candidate / ".env"
        if env_file.is_file() and (candidate / "pyproject.toml").is_file():
            load_dotenv(dotenv_path=env_file)
            return
    load_dotenv()


def missing_required_env_keys() -> list[str]:
    _load_dotenv_from_repo()
    missing: list[str] = []
    for key in REQUIRED_ENV_KEYS:
        value = os.getenv(key)
        if value is None or value.strip() == "":
            missing.append(key)
    return missing


def format_missing_env_message(missing: list[str]) -> str:
    lines = ["Missing required environment variables:"]
    for key in missing:
        lines.append(f"  - {key}")
    lines.append(ENV_HINT)
    return "\n".join(lines)


def require_env_or_exit() -> None:
    missing = missing_required_env_keys()
    if missing:
        print(format_missing_env_message(missing), file=sys.stderr)
        raise SystemExit(1)


def require_env_or_raise() -> None:
    missing = missing_required_env_keys()
    if missing:
        raise RuntimeError(format_missing_env_message(missing))
