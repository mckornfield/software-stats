"""
India job market data — NASSCOM FY2023 Annual Report + MOSPI PLFS 2022-23.

Salaries in INR (Indian Rupees) annual. career_stage: entry/mid/senior.
IT sector employment from NASSCOM; other sectors from MOSPI PLFS and ILO estimates.
Wage growth series 2019–2023 approximate from NASSCOM and government wage statistics.

Sources:
  NASSCOM: https://nasscom.in/knowledge-center/publications/
  MOSPI PLFS: https://mospi.gov.in/plfs-annual-report
"""

import pandas as pd
from ppp_data import to_ppp_usd, to_usd_nominal

# (role, sector, career_stage, median_salary_inr)
_INDIA_SALARIES = [
    ("software_engineer",    "tech",          "entry",   500_000),
    ("software_engineer",    "tech",          "mid",   1_200_000),
    ("software_engineer",    "tech",          "senior",2_500_000),
    ("lawyer",               "legal",         "entry",   300_000),
    ("lawyer",               "legal",         "mid",     600_000),
    ("lawyer",               "legal",         "senior",2_000_000),
    ("physician",            "healthcare",    "entry",   500_000),
    ("physician",            "healthcare",    "mid",     900_000),
    ("physician",            "healthcare",    "senior",2_500_000),
    ("financial_analyst",    "finance",       "entry",   400_000),
    ("financial_analyst",    "finance",       "mid",     750_000),
    ("financial_analyst",    "finance",       "senior",1_800_000),
    ("registered_nurse",     "healthcare",    "entry",   200_000),
    ("registered_nurse",     "healthcare",    "mid",     360_000),
    ("registered_nurse",     "healthcare",    "senior",  600_000),
    ("civil_engineer",       "engineering",   "entry",   350_000),
    ("civil_engineer",       "engineering",   "mid",     600_000),
    ("civil_engineer",       "engineering",   "senior",1_400_000),
    ("construction_laborer", "blue_collar",   "entry",    80_000),
    ("construction_laborer", "blue_collar",   "mid",     120_000),
    ("construction_laborer", "blue_collar",   "senior",  160_000),
    ("farm_worker",          "agriculture",   "entry",    50_000),
    ("farm_worker",          "agriculture",   "mid",      80_000),
    ("farm_worker",          "agriculture",   "senior",  110_000),
    ("manufacturing_worker", "manufacturing", "entry",   120_000),
    ("manufacturing_worker", "manufacturing", "mid",     200_000),
    ("manufacturing_worker", "manufacturing", "senior",  350_000),
    ("retail_worker",        "services",      "entry",   100_000),
    ("retail_worker",        "services",      "mid",     180_000),
    ("retail_worker",        "services",      "senior",  320_000),
]
_INDIA_SALARY_COLS = ["role", "sector", "career_stage", "median_salary_local"]

# (role, w2019, w2020, w2021, w2022, w2023, e2019, e2020, e2021, e2022, e2023)
# w* = median annual wage (INR); e* = employed (thousands)
_INDIA_GROWTH = [
    ("software_engineer",   1_000_000,1_050_000,1_080_000,1_150_000,1_200_000, 4200,4300,4500,5100,5430),
    ("lawyer",                520_000,  540_000,  545_000,  570_000,  600_000, 1800,1820,1840,1860,1880),
    ("physician",             750_000,  750_000,  780_000,  840_000,  900_000, 1200,1230,1250,1270,1300),
    ("financial_analyst",     620_000,  630_000,  660_000,  710_000,  750_000,  600, 580, 620, 660, 700),
    ("registered_nurse",      290_000,  300_000,  310_000,  335_000,  360_000, 3100,3300,3500,3700,3800),
    ("civil_engineer",        500_000,  510_000,  520_000,  560_000,  600_000, 2000,1900,2000,2100,2200),
    ("construction_laborer",   90_000,   85_000,   95_000,  110_000,  120_000,60000,55000,58000,62000,65000),
    ("farm_worker",            60_000,   65_000,   68_000,   74_000,   80_000,200000,195000,196000,198000,200000),
    ("manufacturing_worker",  160_000,  160_000,  170_000,  185_000,  200_000,60000,57000,59000,61000,63000),
    ("retail_worker",         140_000,  140_000,  150_000,  165_000,  180_000,50000,47000,49000,51000,55000),
]
_INDIA_GROWTH_COLS = [
    "role",
    "wage_2019","wage_2020","wage_2021","wage_2022","wage_2023",
    "emp_2019","emp_2020","emp_2021","emp_2022","emp_2023",
]


def get_merged_india_data() -> pd.DataFrame:
    """Return merged India salary + employment + growth DataFrame."""
    sal = pd.DataFrame(_INDIA_SALARIES, columns=_INDIA_SALARY_COLS)
    grw = pd.DataFrame(_INDIA_GROWTH, columns=_INDIA_GROWTH_COLS)
    df = sal.merge(grw, on="role", how="left")
    df["median_salary_ppp_usd"] = df["median_salary_local"].apply(
        lambda x: to_ppp_usd(x, "India")
    )
    df["median_salary_usd"] = df["median_salary_local"].apply(
        lambda x: to_usd_nominal(x, "India")
    )
    df["employed_thousands"] = df["emp_2023"]
    df["yoy_wage_growth_pct"] = (
        (df["wage_2023"] - df["wage_2022"]) / df["wage_2022"] * 100
    ).round(2)
    df["country"] = "India"
    return df
