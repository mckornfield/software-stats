import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ppp_data import to_ppp_usd, to_usd_nominal, PPP_FACTORS, FX_RATES


def test_usa_is_identity():
    assert to_ppp_usd(100_000, "USA") == 100_000


def test_india_conversion():
    # 22 INR per PPP USD => 2_200_000 INR = 100_000 PPP USD
    result = to_ppp_usd(2_200_000, "India")
    assert result == 100_000.0


def test_china_conversion():
    # 4.1 CNY per PPP USD => 410_000 CNY = 100_000 PPP USD
    result = to_ppp_usd(410_000, "China")
    assert result == 100_000.0


def test_all_countries_present():
    assert set(PPP_FACTORS.keys()) == {"USA", "India", "China"}


def test_nominal_usa_is_identity():
    assert to_usd_nominal(100_000, "USA") == 100_000


def test_nominal_india_uses_market_rate():
    # 82.6 INR per USD => 1_200_000 INR = ~14_528 USD
    assert to_usd_nominal(1_200_000, "India") == 14528


def test_nominal_china_uses_market_rate():
    # 7.08 CNY per USD => 200_000 CNY = ~28_249 USD
    assert to_usd_nominal(200_000, "China") == 28249


def test_nominal_is_lower_than_ppp_for_developing():
    # Market rate undervalues local buying power, so nominal < PPP for India/China
    assert to_usd_nominal(1_200_000, "India") < to_ppp_usd(1_200_000, "India")
    assert to_usd_nominal(200_000, "China") < to_ppp_usd(200_000, "China")


def test_fx_rates_present():
    assert set(FX_RATES.keys()) == {"USA", "India", "China"}
