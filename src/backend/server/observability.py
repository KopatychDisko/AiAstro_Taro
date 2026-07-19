"""Optional Langfuse tracing for LangGraph runs (SDK v4)."""

from __future__ import annotations

import os
from typing import List


def _langfuse_keys_present() -> bool:
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if public_key is None or public_key.strip() == "":
        return False
    if secret_key is None or secret_key.strip() == "":
        return False
    return True


def build_langfuse_callbacks(session_id: str, user_name: str) -> List[object]:
    """Return LangChain CallbackHandler list when Langfuse keys are set.

    session_id / user_name are kept for call-site compatibility; trace attributes
    are applied via RunnableConfig metadata (see langfuse_run_metadata).
    """
    _ = (session_id, user_name)
    if not _langfuse_keys_present():
        return []

    from langfuse.langchain import CallbackHandler

    return [CallbackHandler()]


def langfuse_run_metadata(session_id: str, user_name: str) -> dict[str, object]:
    """Metadata keys recognized by Langfuse LangChain integration (v3+/v4)."""
    return {
        "langfuse_session_id": session_id,
        "langfuse_user_id": session_id,
        "langfuse_tags": ["aitaro", "stream"],
        "user_name": user_name,
    }


def flush_langfuse() -> None:
    """Flush pending Langfuse events after a request (no-op when disabled)."""
    if not _langfuse_keys_present():
        return
    from langfuse import get_client

    get_client().flush()
