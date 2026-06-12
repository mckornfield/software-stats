import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from sector_data import get_sector_employment, SECTOR_EMPLOYMENT, SECTORS, SOFTWARE_SECTOR


def test_all_countries_present():
    assert set(SECTOR_EMPLOYMENT.keys()) == {"USA", "India", "China"}


def test_returns_dataframe():
    assert isinstance(get_sector_employment("USA"), pd.DataFrame)


def test_all_sectors_present_each_country():
    for country in ("USA", "India", "China"):
        df = get_sector_employment(country)
        assert set(df["sector"]) == set(SECTORS)


def test_pct_sums_to_100():
    for country in ("USA", "India", "China"):
        df = get_sector_employment(country)
        assert abs(df["pct_of_total"].sum() - 100.0) < 0.5


def test_software_sector_exists():
    df = get_sector_employment("USA")
    assert SOFTWARE_SECTOR in df["sector"].values


def test_india_agriculture_is_largest():
    df = get_sector_employment("India")
    top = df.sort_values("employed_millions", ascending=False).iloc[0]
    assert top["sector"] == "Agriculture"


def test_software_share_reasonable():
    # Software/IT should be a small single-digit % of each whole economy
    for country in ("USA", "India", "China"):
        df = get_sector_employment(country)
        sw = df[df["sector"] == SOFTWARE_SECTOR]["pct_of_total"].values[0]
        assert 0 < sw < 10
