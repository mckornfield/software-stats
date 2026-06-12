"""
Emit the China NBS source tables as raw CSVs.

Sources:
  NBS Statistical Yearbook 2023 (China Statistical Yearbook), Average Wages of
  Employed Persons by Sector. IT sector ("Information Transmission, Software and
  IT Services"): ~CNY201,506/yr.
    https://www.stats.gov.cn/sj/ndsj/2023/indexeh.htm
  NBS Data Explorer: https://data.stats.gov.cn/ (series A0B0C, wages by industry)
  Role-level breakdowns and employment: MIIT sector data, Zhaopin/Boss Zhipin
    salary reports, ILO China labour market brief 2023.

The figures are curated into src/china_data.py (CNY). Running this script writes
them back out as flat CSVs under data/raw/ so the as-sourced tables are
inspectable on disk.

Market FX: 7.08 CNY/USD; PPP: 4.1 CNY/PPP USD (IMF WEO 2023).

Run: python data/raw/fetch_china_nbs.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from china_data import (
    _CHINA_SALARIES, _CHINA_SALARY_COLS,
    _CHINA_GROWTH, _CHINA_GROWTH_COLS,
)

OUT_DIR = ROOT / "data" / "raw"


def main():
    salaries = pd.DataFrame(_CHINA_SALARIES, columns=_CHINA_SALARY_COLS)
    growth = pd.DataFrame(_CHINA_GROWTH, columns=_CHINA_GROWTH_COLS)

    sal_path = OUT_DIR / "china_salaries_2023.csv"
    grw_path = OUT_DIR / "china_growth_2019_2023.csv"
    salaries.to_csv(sal_path, index=False)
    growth.to_csv(grw_path, index=False)

    print(f"Wrote {len(salaries)} salary rows to {sal_path}")
    print(f"Wrote {len(growth)} growth rows to {grw_path}")


if __name__ == "__main__":
    main()
