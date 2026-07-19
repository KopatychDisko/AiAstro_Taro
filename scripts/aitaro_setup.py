"""Console entrypoint for aitaro-setup (env check stub; npm/checklist in Plan 02)."""

from __future__ import annotations

from aitaro_api import ensure_backend_on_path


def main() -> None:
    ensure_backend_on_path()
    from server.required_env import require_env_or_exit

    require_env_or_exit()
