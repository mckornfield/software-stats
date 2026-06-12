import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from usa_data import get_merged_usa_data

EXPECTED_COLS = {
    "role", "sector", "career_stage", "median_salary_local", "median_salary_ppp_usd",
    "median_salary_usd", "employed_thousands", "yoy_wage_growth_pct",
    "wage_2019", "wage_2020", "wage_2021", "wage_2022", "wage_2023",
    "emp_2019", "emp_2020", "emp_2021", "emp_2022", "emp_2023",
    "country",
}


def test_returns_dataframe():
    df = get_merged_usa_data()
    assert isinstance(df, pd.DataFrame)


def test_has_expected_columns():
    df = get_merged_usa_data()
    assert EXPECTED_COLS.issubset(set(df.columns))


def test_country_is_usa():
    df = get_merged_usa_data()
    assert (df["country"] == "USA").all()


def test_swe_mid_salary():
    df = get_merged_usa_data()
    swe_mid = df[(df["role"] == "software_engineer") & (df["career_stage"] == "mid")]
    assert len(swe_mid) == 1
    assert swe_mid.iloc[0]["median_salary_local"] == 130160


def test_ppp_usd_equals_local_for_usa():
    df = get_merged_usa_data()
    assert (df["median_salary_local"] == df["median_salary_ppp_usd"]).all()


def test_nominal_usd_equals_local_for_usa():
    df = get_merged_usa_data()
    assert (df["median_salary_local"] == df["median_salary_usd"]).all()


def test_no_null_salaries():
    df = get_merged_usa_data()
    assert df["median_salary_local"].notna().all()


def test_has_all_roles():
    df = get_merged_usa_data()
    expected_roles = {
        "software_engineer", "lawyer", "physician", "financial_analyst",
        "registered_nurse", "civil_engineer", "construction_laborer",
        "farm_worker", "manufacturing_worker", "retail_worker",
    }
    assert expected_roles.issubset(set(df["role"].unique()))
