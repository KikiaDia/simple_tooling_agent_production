import json

from simple_agent.tools import classify_price_tier_json


def test_tool_returns_expected_json() -> None:
    result = json.loads(classify_price_tier_json(150))
    assert result["tier"] == "Mid-Range"
    assert result["price"] == 150
    assert "percentile_band" in result
