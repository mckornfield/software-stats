import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from india_data import get_merged_india_data


def test_returns_dataframe():
    df = get_merged_india_data()
    assert isinstance(df, pd.DataFrame)


def test_country_is_india():
    df = get_merged_india_data()
    assert (df["country"] == "India").all()


def test_ppp_usd_is_less_than_local_inr():
    df = get_merged_india_data()
    assert (df["median_salary_ppp_usd"] < df["median_salary_local"]).all()


def test_swe_mid_ppp_usd():
    df = get_merged_india_data()
    swe_mid = df[(df["role"] == "software_engineer") & (df["career_stage"] == "mid")]
    # 1_200_000 INR / 22 = 54545 PPP USD
    assert abs(swe_mid.iloc[0]["median_salary_ppp_usd"] - 54545) < 100


def test_no_null_salaries():
    df = get_merged_india_data()
    assert df["median_salary_local"].notna().all()
