import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ppp_data import to_ppp_usd, PPP_FACTORS


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
