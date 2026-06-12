"""
China job market data — NBS 2023 Statistical Yearbook + MIIT sector data.

Salaries in CNY (Chinese Yuan Renminbi) annual. career_stage: entry/mid/senior.
IT sector: NBS average wages for "Information Transmission, Software and IT Services".
Other sectors from NBS industry wage statistics and ILO country reports.

Sources:
  NBS Statistical Yearbook 2023: https://www.stats.gov.cn/sj/ndsj/2023/indexeh.htm
  NBS: https://data.stats.gov.cn/
"""

import pandas as pd
from ppp_data import to_ppp_usd

# (role, sector, career_stage, median_salary_cny)
_CHINA_SALARIES = [
    ("software_engineer",    "tech",          "entry",   90_000),
    ("software_engineer",    "tech",          "mid",    200_000),
    ("software_engineer",    "tech",          "senior", 450_000),
    ("lawyer",               "legal",         "entry",   80_000),
    ("lawyer",               "legal",         "mid",    150_000),
    ("lawyer",               "legal",         "senior", 350_000),
    ("physician",            "healthcare",    "entry",   90_000),
    ("physician",            "healthcare",    "mid",    180_000),
    ("physician",            "healthcare",    "senior", 360_000),
    ("financial_analyst",    "finance",       "entry",   90_000),
    ("financial_analyst",    "finance",       "mid",    160_000),
    ("financial_analyst",    "finance",       "senior", 320_000),
    ("registered_nurse",     "healthcare",    "entry",   55_000),
    ("registered_nurse",     "healthcare",    "mid",     90_000),
    ("registered_nurse",     "healthcare",    "senior", 150_000),
    ("civil_engineer",       "engineering",   "entry",   75_000),
    ("civil_engineer",       "engineering",   "mid",    130_000),
    ("civil_engineer",       "engineering",   "senior", 260_000),
    ("construction_laborer", "blue_collar",   "entry",   40_000),
    ("construction_laborer", "blue_collar",   "mid",     60_000),
    ("construction_laborer", "blue_collar",   "senior",  85_000),
    ("farm_worker",          "agriculture",   "entry",   18_000),
    ("farm_worker",          "agriculture",   "mid",     28_000),
    ("farm_worker",          "agriculture",   "senior",  40_000),
    ("manufacturing_worker", "manufacturing", "entry",   45_000),
    ("manufacturing_worker", "manufacturing", "mid",     65_000),
    ("manufacturing_worker", "manufacturing", "senior", 100_000),
    ("retail_worker",        "services",      "entry",   38_000),
    ("retail_worker",        "services",      "mid",     55_000),
    ("retail_worker",        "services",      "senior",  85_000),
]
_CHINA_SALARY_COLS = ["role", "sector", "career_stage", "median_salary_local"]

# (role, w2019, w2020, w2021, w2022, w2023, e2019, e2020, e2021, e2022, e2023)
# w* = median annual wage (CNY); e* = employed (thousands)
_CHINA_GROWTH = [
    ("software_engineer",   163_000,177_000,194_000,200_000,201_500, 7800, 8200, 9100, 9600,10000),
    ("lawyer",              125_000,130_000,138_000,145_000,150_000,  510,  530,  555,  565,  570),
    ("physician",           153_000,155_000,163_000,173_000,180_000, 3700, 3800, 3980, 4090, 4200),
    ("financial_analyst",   135_000,140_000,148_000,155_000,160_000, 1200, 1180, 1220, 1260, 1300),
    ("registered_nurse",     72_000, 78_000, 82_000, 86_000, 90_000, 4440, 4700, 5010, 5220, 5500),
    ("civil_engineer",      107_000,113_000,119_000,125_000,130_000, 5900, 5800, 5900, 6000, 6100),
    ("construction_laborer", 49_000, 52_000, 55_000, 58_000, 60_000,58000,56000,57000,55000,53000),
    ("farm_worker",          22_000, 23_000, 25_000, 27_000, 28_000,194000,191000,188000,185000,180000),
    ("manufacturing_worker", 55_000, 57_000, 60_000, 63_000, 65_000,99000,97000,99000,100000,100000),
    ("retail_worker",        47_000, 48_000, 50_000, 52_000, 55_000,55000,52000,54000,55000,56000),
]
_CHINA_GROWTH_COLS = [
    "role",
    "wage_2019","wage_2020","wage_2021","wage_2022","wage_2023",
    "emp_2019","emp_2020","emp_2021","emp_2022","emp_2023",
]


def get_merged_china_data() -> pd.DataFrame:
    """Return merged China salary + employment + growth DataFrame."""
    sal = pd.DataFrame(_CHINA_SALARIES, columns=_CHINA_SALARY_COLS)
    grw = pd.DataFrame(_CHINA_GROWTH, columns=_CHINA_GROWTH_COLS)
    df = sal.merge(grw, on="role", how="left")
    df["median_salary_ppp_usd"] = df["median_salary_local"].apply(
        lambda x: to_ppp_usd(x, "China")
    )
    df["employed_thousands"] = df["emp_2023"]
    df["yoy_wage_growth_pct"] = (
        (df["wage_2023"] - df["wage_2022"]) / df["wage_2022"] * 100
    ).round(2)
    df["country"] = "China"
    return df
