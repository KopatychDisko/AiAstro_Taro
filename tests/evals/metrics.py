"""DeepEval metrics for offline router + taro evals (no Confident AI)."""

from __future__ import annotations

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class ExactMatchMetric(BaseMetric):
    """Deterministic string match — offline, no LLM judge."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.score: float = 0.0
        self.success: bool = False
        self.reason: str = ""
        self.error: str | None = None

    def measure(self, test_case: LLMTestCase) -> float:
        actual = test_case.actual_output
        expected = test_case.expected_output
        matched = actual == expected
        self.score = 1.0 if matched else 0.0
        self.success = self.score >= self.threshold
        if matched:
            self.reason = "actual_output matches expected_output"
        else:
            self.reason = (
                f"expected {expected!r} but got {actual!r}"
            )
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self) -> str:
        return "ExactMatchMetric"


ROUTER_METRICS: list[BaseMetric] = [ExactMatchMetric(threshold=1.0)]
TARO_METRICS: list[BaseMetric] = [ExactMatchMetric(threshold=1.0)]
