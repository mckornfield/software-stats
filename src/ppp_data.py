"""
Currency conversion factors for cross-country comparison.

Two distinct conversions are provided:

- to_usd_nominal: market exchange rate. Answers "what does this paycheck
  convert to in dollars?" Good for showing the raw global pay gap.
- to_ppp_usd: purchasing-power-parity rate. Answers "how much local buying
  power does this provide, in dollars?" Already reflects cost-of-living
  differences, so it is the right basis for comparing living standards.

Sources: IMF World Economic Outlook 2023 (PPP factors), IMF/World Bank 2023
annual average market exchange rates.
"""

# Local currency units per 1 PPP USD (2023 IMF WEO)
PPP_FACTORS: dict[str, float] = {
    "USA":   1.0,    # USD is the base
    "India": 22.0,   # 22 INR = 1 PPP USD
    "China":  4.1,   # 4.1 CNY = 1 PPP USD
}

# Local currency units per 1 USD at market exchange rate (2023 annual average)
FX_RATES: dict[str, float] = {
    "USA":    1.0,    # USD is the base
    "India": 82.6,    # 82.6 INR = 1 USD
    "China":  7.08,   # 7.08 CNY = 1 USD
}


def to_ppp_usd(amount_local: float, country: str) -> float:
    """Convert a local-currency amount to PPP-adjusted USD (local buying power)."""
    return round(amount_local / PPP_FACTORS[country], 0)


def to_usd_nominal(amount_local: float, country: str) -> float:
    """Convert a local-currency amount to USD at the market exchange rate."""
    return round(amount_local / FX_RATES[country], 0)
