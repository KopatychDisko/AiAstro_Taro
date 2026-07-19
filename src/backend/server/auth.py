import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()


async def verify_stream_api_key(
    x_api_key: str | None = Header(None, alias="X-API-Key"),
    authorization: str | None = Header(None),
) -> None:
    expected = os.getenv("STREAM_API_KEY")
    if expected is None or expected == "":
        raise HTTPException(
            status_code=500,
            detail="STREAM_API_KEY not configured",
        )

    provided = x_api_key
    if provided is None and authorization is not None:
        prefix = "Bearer "
        if authorization.startswith(prefix):
            provided = authorization[len(prefix):]

    if provided is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not secrets.compare_digest(provided, expected):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
