import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from china_data import get_merged_china_data


def test_returns_dataframe():
    df = get_merged_china_data()
    assert isinstance(df, pd.DataFrame)


def test_country_is_china():
    df = get_merged_china_data()
    assert (df["country"] == "China").all()


def test_ppp_usd_is_less_than_local_cny():
    df = get_merged_china_data()
    assert (df["median_salary_ppp_usd"] < df["median_salary_local"]).all()


def test_swe_mid_salary():
    df = get_merged_china_data()
    swe_mid = df[(df["role"] == "software_engineer") & (df["career_stage"] == "mid")]
    assert swe_mid.iloc[0]["median_salary_local"] == 200_000


def test_no_null_salaries():
    df = get_merged_china_data()
    assert df["median_salary_local"].notna().all()
