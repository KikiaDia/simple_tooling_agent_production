import json

from simple_agent.domain import classify_price_tier


def classify_price_tier_json(price: float) -> str:
    """Deterministic tool implementation used by tests and the fake backend."""
    result = classify_price_tier(price)
    return json.dumps(
        {
            "price": result.price,
            "tier": result.tier,
            "percentile_band": result.percentile_band,
            "interpretation": result.interpretation,
        }
    )


def classify_price_tier_uc(price: float) -> str:
    """Function intended to be registered as a Unity Catalog Python function.

    Args:
        price: Nightly listing price in USD.

    Returns:
        JSON string with the price tier and market interpretation.
    """
    return classify_price_tier_json(price)
