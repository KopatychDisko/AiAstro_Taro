"""Console entrypoint for aitaro-setup: env fail-fast, tarot MCP npm build, checklist."""

from __future__ import annotations

import subprocess
from pathlib import Path

from aitaro_api import ensure_backend_on_path


def build_tarot_mcp(repo_root: Path) -> None:
    tarotmcp = repo_root / "src" / "tarotmcp"
    if not tarotmcp.is_dir():
        raise FileNotFoundError(f"Missing tarot MCP directory: {tarotmcp}")
    subprocess.run(["npm", "install"], cwd=tarotmcp, check=True)
    subprocess.run(["npm", "run", "build"], cwd=tarotmcp, check=True)


def _print_checklist() -> None:
    print("Tarot MCP build: OK")
    print("Required env: OK (STREAM_API_KEY, OPENAI_API_KEY, ZEP_API)")
    print()
    print("Next:")
    print("  uv run aitaro-api")
    print()
    print("UI (optional; needs POSTGRESQL_* in .env):")
    print("  cd src/frontend && uv run streamlit run login_menu.py")


def main() -> None:
    repo_root = ensure_backend_on_path()
    from server.required_env import require_env_or_exit

    require_env_or_exit()
    build_tarot_mcp(repo_root)
    _print_checklist()
