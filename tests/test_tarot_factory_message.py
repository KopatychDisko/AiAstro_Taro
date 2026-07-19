"""SC-10.4: tarot factory missing-dist error points at aitaro-setup."""

from __future__ import annotations

import pytest

from agents.taro import factory as tarot_factory


@pytest.mark.asyncio
async def test_create_tarot_agent_missing_dist_mentions_aitaro_setup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tarot_factory.os.path, "isfile", lambda path: False)
    with pytest.raises(FileNotFoundError, match="aitaro-setup") as exc_info:
        await tarot_factory.create_tarot_agent()
    message = str(exc_info.value)
    assert "uv run aitaro-setup" in message
