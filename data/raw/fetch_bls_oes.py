"""
Emit the USA BLS OES source tables as raw CSVs.

Source: U.S. Bureau of Labor Statistics, Occupational Employment and Wage
Statistics (OES) May 2023.
  Landing page: https://www.bls.gov/oes/current/oes_nat.htm
  Bulk download: https://www.bls.gov/oes/special.requests/oesm23nat.zip

The figures are curated from the OES national release for the SOC codes below
and embedded in src/usa_data.py. Running this script writes them back out as
flat CSVs under data/raw/ so the as-sourced tables are inspectable on disk.

SOC codes:
  15-1252 Software Developers | 23-1011 Lawyers | 29-1210x Physicians
  13-2051 Financial Analysts  | 29-1141 Registered Nurses | 17-2051 Civil Engineers
  47-2061 Construction Laborers | 45-2092 Farmworkers | 51-XXXX Production
  41-2031 Retail Salespersons

To refresh from source: download oesm23nat.zip, open all_data_M_2023.xlsx,
read annual median wage and tot_emp per SOC code, then update the tables in
src/usa_data.py.

Run: python data/raw/fetch_bls_oes.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from usa_data import (
    _USA_SALARIES, _USA_SALARY_COLS,
    _USA_GROWTH, _USA_GROWTH_COLS,
)

OUT_DIR = ROOT / "data" / "raw"


def main():
    salaries = pd.DataFrame(_USA_SALARIES, columns=_USA_SALARY_COLS)
    growth = pd.DataFrame(_USA_GROWTH, columns=_USA_GROWTH_COLS)

    sal_path = OUT_DIR / "usa_oes_salaries_2023.csv"
    grw_path = OUT_DIR / "usa_oes_growth_2019_2023.csv"
    salaries.to_csv(sal_path, index=False)
    growth.to_csv(grw_path, index=False)

    print(f"Wrote {len(salaries)} salary rows to {sal_path}")
    print(f"Wrote {len(growth)} growth rows to {grw_path}")


if __name__ == "__main__":
    main()
