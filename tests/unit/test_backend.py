import pytest

from simple_agent.backends import FakeAgentBackend


@pytest.mark.asyncio
async def test_fake_backend_calls_tool_for_price() -> None:
    result = await FakeAgentBackend().invoke("Is $150/night a good deal?")
    assert result.tool_calls == 1
    assert "Mid-Range" in result.answer


@pytest.mark.asyncio
async def test_fake_backend_supports_multiple_prices() -> None:
    result = await FakeAgentBackend().invoke("Classify $80, $200 and $350")
    assert result.tool_calls == 3
    assert "Budget" in result.answer
    assert "Premium" in result.answer
    assert "Luxury" in result.answer
