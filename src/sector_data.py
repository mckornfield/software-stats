"""
Economy-wide employment by sector for USA, India, and China (2023, approximate).

Unlike the per-role tables in usa_data/india_data/china_data (which cover 10
tracked occupations), this module gives total employment across each WHOLE
economy, broken into broad sectors. This lets charts show the true software/IT
slice of national employment, not just its share among the tracked roles.

Figures are approximate 2023 totals in millions of workers, curated from:
  USA   — BLS Current Employment Statistics (CES) + Employment Situation 2023
          (~161M employed). https://www.bls.gov/ces/
  India — MOSPI Periodic Labour Force Survey (PLFS) 2022-23 broad-sector shares
          applied to ~500M employed. https://mospi.gov.in/plfs-annual-report
  China — NBS Statistical Yearbook 2023 employment by sector (~740M employed).
          https://www.stats.gov.cn/sj/ndsj/2023/indexeh.htm

Sector buckets are harmonized across countries so they can be compared directly.
"Information & Software/IT" is the software/tech slice.
"""

import pandas as pd

SECTORS = [
    "Agriculture",
    "Manufacturing",
    "Construction",
    "Information & Software/IT",
    "Finance & Insurance",
    "Healthcare & Social",
    "Professional & Legal Services",
    "Trade (Retail & Wholesale)",
    "Education",
    "Public Administration",
    "Other Services",
]

# country -> {sector: employed_millions}, 2023 approximate
SECTOR_EMPLOYMENT: dict[str, dict[str, float]] = {
    "USA": {
        "Agriculture": 2.4,
        "Manufacturing": 13.0,
        "Construction": 8.0,
        "Information & Software/IT": 5.0,
        "Finance & Insurance": 6.8,
        "Healthcare & Social": 21.5,
        "Professional & Legal Services": 22.0,
        "Trade (Retail & Wholesale)": 21.0,
        "Education": 14.0,
        "Public Administration": 7.3,
        "Other Services": 40.0,
    },
    "India": {
        "Agriculture": 230.0,
        "Manufacturing": 60.0,
        "Construction": 70.0,
        "Information & Software/IT": 5.4,
        "Finance & Insurance": 7.0,
        "Healthcare & Social": 8.0,
        "Professional & Legal Services": 12.0,
        "Trade (Retail & Wholesale)": 55.0,
        "Education": 20.0,
        "Public Administration": 12.0,
        "Other Services": 20.0,
    },
    "China": {
        "Agriculture": 170.0,
        "Manufacturing": 120.0,
        "Construction": 55.0,
        "Information & Software/IT": 10.0,
        "Finance & Insurance": 7.0,
        "Healthcare & Social": 13.0,
        "Professional & Legal Services": 20.0,
        "Trade (Retail & Wholesale)": 150.0,
        "Education": 18.0,
        "Public Administration": 25.0,
        "Other Services": 150.0,
    },
}

SOFTWARE_SECTOR = "Information & Software/IT"


def get_sector_employment(country: str) -> pd.DataFrame:
    """Return economy-wide sector employment for a country with % of total."""
    data = SECTOR_EMPLOYMENT[country]
    df = pd.DataFrame(
        [{"sector": s, "employed_millions": data[s]} for s in SECTORS]
    )
    df["country"] = country
    total = df["employed_millions"].sum()
    df["pct_of_total"] = (df["employed_millions"] / total * 100).round(2)
    return df
