"""
Emit the India NASSCOM/MOSPI source tables as raw CSVs.

Sources:
  NASSCOM Strategic Review 2023 (IT-BPM sector: ~5.43M employees, avg ~Rs1.2M/yr)
    https://nasscom.in/knowledge-center/publications/
  MOSPI Periodic Labour Force Survey (PLFS) 2022-23 (sector employment, earnings)
    https://mospi.gov.in/plfs-annual-report
  Non-IT role salaries: PayScale India 2023, ASSOCHAM healthcare survey,
    Bar Council of India statistics.

The figures are curated into src/india_data.py (INR). Running this script writes
them back out as flat CSVs under data/raw/ so the as-sourced tables are
inspectable on disk.

Market FX: 82.6 INR/USD; PPP: 22 INR/PPP USD (IMF WEO 2023).

Run: python data/raw/fetch_india_nasscom.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from india_data import (
    _INDIA_SALARIES, _INDIA_SALARY_COLS,
    _INDIA_GROWTH, _INDIA_GROWTH_COLS,
)

OUT_DIR = ROOT / "data" / "raw"


def main():
    salaries = pd.DataFrame(_INDIA_SALARIES, columns=_INDIA_SALARY_COLS)
    growth = pd.DataFrame(_INDIA_GROWTH, columns=_INDIA_GROWTH_COLS)

    sal_path = OUT_DIR / "india_salaries_2023.csv"
    grw_path = OUT_DIR / "india_growth_2019_2023.csv"
    salaries.to_csv(sal_path, index=False)
    growth.to_csv(grw_path, index=False)

    print(f"Wrote {len(salaries)} salary rows to {sal_path}")
    print(f"Wrote {len(growth)} growth rows to {grw_path}")


if __name__ == "__main__":
    main()
