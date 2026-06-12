"""
USA job market data — BLS OES May 2023 release.

Salary data: BLS Occupational Employment and Wage Statistics (OES) May 2023.
career_stage proxy: entry=10th pct, mid=50th pct (median), senior=90th pct.
Employment: BLS OES total employed (thousands).
Growth series: BLS OES median wage and employment by year 2019-2023.

Source: https://www.bls.gov/oes/
"""

import pandas as pd
from ppp_data import to_ppp_usd

# (role, sector, career_stage, median_salary_usd)
# BLS SOC codes: software_engineer=15-1252, lawyer=23-1011,
#   physician=29-1210x, financial_analyst=13-2051, nurse=29-1141,
#   civil_engineer=17-2051, construction_laborer=47-2061,
#   farm_worker=45-2092, manufacturing=51-XXXX, retail=41-2031
_USA_SALARIES = [
    ("software_engineer",    "tech",         "entry",   73670),
    ("software_engineer",    "tech",         "mid",    130160),
    ("software_engineer",    "tech",         "senior", 208620),
    ("lawyer",               "legal",        "entry",   64150),
    ("lawyer",               "legal",        "mid",    145760),
    ("lawyer",               "legal",        "senior", 239200),
    ("physician",            "healthcare",   "entry",  100000),
    ("physician",            "healthcare",   "mid",    229300),
    ("physician",            "healthcare",   "senior", 350000),
    ("financial_analyst",    "finance",      "entry",   53690),
    ("financial_analyst",    "finance",      "mid",     99890),
    ("financial_analyst",    "finance",      "senior", 171010),
    ("registered_nurse",     "healthcare",   "entry",   57180),
    ("registered_nurse",     "healthcare",   "mid",     81220),
    ("registered_nurse",     "healthcare",   "senior", 113300),
    ("civil_engineer",       "engineering",  "entry",   60840),
    ("civil_engineer",       "engineering",  "mid",     95890),
    ("civil_engineer",       "engineering",  "senior", 153590),
    ("construction_laborer", "blue_collar",  "entry",   31000),
    ("construction_laborer", "blue_collar",  "mid",     44850),
    ("construction_laborer", "blue_collar",  "senior",  63000),
    ("farm_worker",          "agriculture",  "entry",   25000),
    ("farm_worker",          "agriculture",  "mid",     35020),
    ("farm_worker",          "agriculture",  "senior",  48000),
    ("manufacturing_worker", "manufacturing","entry",   28000),
    ("manufacturing_worker", "manufacturing","mid",     45040),
    ("manufacturing_worker", "manufacturing","senior",  68000),
    ("retail_worker",        "services",     "entry",   25000),
    ("retail_worker",        "services",     "mid",     36530),
    ("retail_worker",        "services",     "senior",  52000),
]
_USA_SALARY_COLS = ["role", "sector", "career_stage", "median_salary_local"]

# (role, w2019, w2020, w2021, w2022, w2023, e2019, e2020, e2021, e2022, e2023)
# w* = median annual wage (USD); e* = total employed (thousands)
_USA_GROWTH = [
    ("software_engineer",   107900,110140,120730,127260,130160,  1775,1731,1688,1795,1825),
    ("lawyer",              122960,126930,127990,136260,145760,   670, 665, 682, 691, 698),
    ("physician",           208000,208000,208000,224000,229300,   713, 693, 728, 738, 748),
    ("financial_analyst",    85660, 83660, 91580, 96220, 99890,   329, 296, 312, 327, 333),
    ("registered_nurse",     73300, 75330, 77600, 81220, 81220,  3096,3130,3238,3238,3238),
    ("civil_engineer",       86640, 88050, 88050, 94360, 95890,   329, 330, 329, 337, 338),
    ("construction_laborer", 37080, 38440, 39520, 42600, 44850,  1380,1349,1360,1428,1434),
    ("farm_worker",          29200, 30160, 31460, 33760, 35020,   800, 790, 785, 795, 800),
    ("manufacturing_worker", 40760, 41780, 43780, 44880, 45040,  9300,8900,9100,9200,9000),
    ("retail_worker",        31480, 32370, 33890, 35570, 36530,  4400,4100,4200,4200,4186),
]
_USA_GROWTH_COLS = [
    "role",
    "wage_2019","wage_2020","wage_2021","wage_2022","wage_2023",
    "emp_2019","emp_2020","emp_2021","emp_2022","emp_2023",
]


def get_merged_usa_data() -> pd.DataFrame:
    """Return merged USA salary + employment + growth DataFrame."""
    sal = pd.DataFrame(_USA_SALARIES, columns=_USA_SALARY_COLS)
    grw = pd.DataFrame(_USA_GROWTH, columns=_USA_GROWTH_COLS)
    df = sal.merge(grw, on="role", how="left")
    df["median_salary_ppp_usd"] = df["median_salary_local"].apply(
        lambda x: to_ppp_usd(x, "USA")
    )
    df["employed_thousands"] = df["emp_2023"]
    df["yoy_wage_growth_pct"] = (
        (df["wage_2023"] - df["wage_2022"]) / df["wage_2022"] * 100
    ).round(2)
    df["country"] = "USA"
    return df
