from dataclasses import dataclass


@dataclass(frozen=True)
class PriceTier:
    price: float
    tier: str
    percentile_band: str
    interpretation: str


def classify_price_tier(price: float) -> PriceTier:
    if price < 0:
        raise ValueError("price must be >= 0")

    tiers = [
        (100.0, "Budget", "bottom 25%", "Well below the SF market average."),
        (175.0, "Mid-Range", "25-50%", "Around the SF market median."),
        (300.0, "Premium", "50-75%", "Above average for SF listings."),
        (float("inf"), "Luxury", "top 25%", "Among the most expensive listings in SF."),
    ]

    for threshold, tier, band, interpretation in tiers:
        if price < threshold:
            return PriceTier(
                price=price,
                tier=tier,
                percentile_band=band,
                interpretation=interpretation,
            )
    raise AssertionError("unreachable")
