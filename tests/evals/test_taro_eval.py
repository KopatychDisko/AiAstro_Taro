"""Offline DeepEval suite for taro MCP spread-name mapping (no LLM)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from agents.cards.mapping import parse_mcp_reading_text
from tests.evals.metrics import TARO_METRICS

GOLDENS_PATH = Path(__file__).resolve().parent / "goldens_taro.json"


def load_taro_goldens(path: Path) -> list[dict[str, str]]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError(f"Taro goldens must be a JSON list: {path}")
    goldens: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise TypeError(f"Taro golden must be an object: {item!r}")
        if "input" not in item or "expected_output" not in item:
            raise KeyError(f"Taro golden missing input/expected_output: {item!r}")
        goldens.append(
            {
                "input": str(item["input"]),
                "expected_output": str(item["expected_output"]),
            }
        )
    return goldens


TARO_GOLDENS = load_taro_goldens(GOLDENS_PATH)


def run_taro_mapping(mcp_markdown: str) -> str:
    """Map MCP reading markdown to frontend spread_name."""
    _cards, spread_name = parse_mcp_reading_text(mcp_markdown)
    return spread_name


@pytest.mark.eval
@pytest.mark.parametrize("golden", TARO_GOLDENS)
def test_taro_eval(golden: dict[str, str]) -> None:
    actual_output = run_taro_mapping(golden["input"])
    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=actual_output,
        expected_output=golden["expected_output"],
    )
    assert_test(test_case=test_case, metrics=TARO_METRICS)
