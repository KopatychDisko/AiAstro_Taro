"""Optional Langfuse tracing for LangGraph runs."""

from __future__ import annotations

import os
from typing import List


def build_langfuse_callbacks(session_id: str, user_name: str) -> List[object]:
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST")

    if public_key is None or public_key == "":
        return []
    if secret_key is None or secret_key == "":
        return []

    from langfuse.langchain import CallbackHandler

    handler_kwargs: dict[str, str] = {
        "session_id": session_id,
        "user_id": session_id,
    }
    if host is not None and host != "":
        handler_kwargs["host"] = host

    handler = CallbackHandler(
        **handler_kwargs,
        metadata={"user_name": user_name},
    )
    return [handler]
