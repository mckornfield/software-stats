"""
Emit economy-wide sector employment tables as raw CSVs.

Sources (2023, approximate totals in millions of workers):
  USA   — BLS Current Employment Statistics + Employment Situation (~161M employed)
          https://www.bls.gov/ces/
  India — MOSPI PLFS 2022-23 broad-sector shares on ~500M employed
          https://mospi.gov.in/plfs-annual-report
  China — NBS Statistical Yearbook 2023 employment by sector (~740M employed)
          https://www.stats.gov.cn/sj/ndsj/2023/indexeh.htm

Figures are curated into src/sector_data.py. Running this script writes them
back out as flat per-country CSVs under data/raw/ for inspection on disk.

Run: python data/raw/fetch_sector_employment.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from sector_data import get_sector_employment

OUT_DIR = ROOT / "data" / "raw"


def main():
    for country in ("USA", "India", "China"):
        df = get_sector_employment(country)
        out = OUT_DIR / f"{country.lower()}_sector_employment_2023.csv"
        df.to_csv(out, index=False)
        print(f"Wrote {len(df)} sector rows to {out}")


if __name__ == "__main__":
    main()
