import pytest

from simple_agent.domain import classify_price_tier


@pytest.mark.parametrize(
    ("price", "expected"),
    [
        (0, "Budget"),
        (99.99, "Budget"),
        (100, "Mid-Range"),
        (174.99, "Mid-Range"),
        (175, "Premium"),
        (299.99, "Premium"),
        (300, "Luxury"),
        (500, "Luxury"),
    ],
)
def test_classify_price_tier_boundaries(price: float, expected: str) -> None:
    assert classify_price_tier(price).tier == expected


def test_negative_price_rejected() -> None:
    with pytest.raises(ValueError, match="price must be >= 0"):
        classify_price_tier(-1)
