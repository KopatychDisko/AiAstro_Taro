"""Stream endpoint tests with mocked workflow."""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from unittest.mock import MagicMock

import pytest
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

from server.auth import verify_stream_api_key
from server.schemas import ExtractData, UserData


def _build_test_app(mock_stream_agent):
    @asynccontextmanager
    async def mock_lifespan(app: FastAPI):
        yield

    test_app = FastAPI(lifespan=mock_lifespan)

    @test_app.post("/stream")
    async def stream_route(
        item: UserData,
        _: None = Depends(verify_stream_api_key),
    ):
        return StreamingResponse(mock_stream_agent(item), media_type="application/json")

    return test_app


@pytest.fixture
def stream_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("STREAM_API_KEY", "test-stream-key")

    async def mock_stream_agent(item: UserData):
        chunk = ExtractData(
            next_node="END",
            message_to_user="Hello from test",
        )
        yield chunk.model_dump_json()

    test_app = _build_test_app(mock_stream_agent)

    with TestClient(test_app) as client:
        yield client


def test_stream_returns_200_and_valid_extract_data_chunks(
    stream_client: TestClient,
) -> None:
    body = {
        "message": "hi",
        "user_id": "1",
        "country": "France",
        "city": "Paris",
        "birth_day": "1990-01-01",
        "time_birth": "12:00",
        "name": "Test",
    }

    response = stream_client.post(
        "/stream",
        json=body,
        headers={"X-API-Key": os.environ["STREAM_API_KEY"]},
    )

    assert response.status_code == 200

    chunks = [line for line in response.text.splitlines() if line.strip()]
    assert len(chunks) >= 1

    for raw in chunks:
        data = ExtractData.model_validate(json.loads(raw))
        assert data.message_to_user is not None


def test_stream_rejects_missing_api_key(stream_client: TestClient) -> None:
    body = {
        "message": "hi",
        "user_id": "1",
        "country": "France",
        "city": "Paris",
        "birth_day": "1990-01-01",
        "time_birth": "12:00",
        "name": "Test",
    }

    response = stream_client.post("/stream", json=body)

    assert response.status_code == 401
