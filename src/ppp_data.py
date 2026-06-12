"""IMF 2023 PPP conversion factors. Source: IMF World Economic Outlook 2023."""

# Local currency units per 1 PPP USD (2023 IMF WEO)
PPP_FACTORS: dict[str, float] = {
    "USA":   1.0,    # USD is the base
    "India": 22.0,   # 22 INR = 1 PPP USD
    "China":  4.1,   # 4.1 CNY = 1 PPP USD
}


def to_ppp_usd(amount_local: float, country: str) -> float:
    """Convert a local-currency amount to PPP-adjusted USD."""
    return round(amount_local / PPP_FACTORS[country], 0)
