"""Offline DeepEval suite for router next_node routing (mocked LLM)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from tests.conftest import make_mock_agents, make_mock_zep, make_router_output
from tests.evals.metrics import ROUTER_METRICS

GOLDENS_PATH = Path(__file__).resolve().parent / "goldens_router.json"


def load_router_goldens(path: Path) -> list[dict[str, str]]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError(f"Router goldens must be a JSON list: {path}")
    goldens: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise TypeError(f"Router golden must be an object: {item!r}")
        if "input" not in item or "expected_output" not in item:
            raise KeyError(f"Router golden missing input/expected_output: {item!r}")
        goldens.append(
            {
                "input": str(item["input"]),
                "expected_output": str(item["expected_output"]),
            }
        )
    return goldens


ROUTER_GOLDENS = load_router_goldens(GOLDENS_PATH)


def _graph_input(user_message: str) -> dict[str, object]:
    return {
        "messages": [HumanMessage(content=user_message)],
        "name": "Test",
        "birth_day": "1990-01-01",
        "time_birth": "12:00",
        "city": "Paris",
        "country": "France",
        "next_node": "router_node",
    }


async def run_router_with_mocks(
    user_message: str,
    expected_next_node: str,
) -> str:
    """Drive router_node with mocked structured output; return next_node."""
    router_output = make_router_output(next_node=expected_next_node, message=None)
    if expected_next_node == "add_memory":
        router_output = make_router_output(
            next_node=expected_next_node,
            message="General chat reply",
        )
    mock_agents = make_mock_agents(router_output)
    mock_zep = make_mock_zep()

    with (
        patch("agents.workflow.create_agents", AsyncMock(return_value=mock_agents)),
        patch("agents.workflow.AsyncZep", return_value=mock_zep),
    ):
        from agents.workflow import setup_workflow

        compiled = await setup_workflow()
        config = RunnableConfig(configurable={"thread_id": "eval-router-1"})
        router_update: dict[str, object] | None = None

        async for update in compiled.astream(
            _graph_input(user_message),
            config=config,
            stream_mode="updates",
        ):
            if "router_node" in update:
                router_update = update["router_node"]
                break

    if router_update is None:
        raise RuntimeError("router_node did not emit an update")
    next_node = router_update.get("next_node")
    if not isinstance(next_node, str):
        raise TypeError(f"router next_node must be str, got {next_node!r}")
    return next_node


@pytest.mark.eval
@pytest.mark.asyncio
@pytest.mark.parametrize("golden", ROUTER_GOLDENS)
async def test_router_eval(golden: dict[str, str]) -> None:
    actual_output = await run_router_with_mocks(
        golden["input"],
        golden["expected_output"],
    )
    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=actual_output,
        expected_output=golden["expected_output"],
    )
    assert_test(test_case=test_case, metrics=ROUTER_METRICS)
