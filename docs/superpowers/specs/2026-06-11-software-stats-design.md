# software-stats Design Spec
**Date:** 2026-06-11  
**Status:** Approved

## Overview

Analyze software engineering job markets in the USA, India, and China. Compare SWE pay and employment to equivalent-education professional roles (lawyer, doctor, nurse, financial analyst) and to blue-collar/agricultural roles. Show where SWEs are best/worst off relative to their peers, adjusted for purchasing power parity.

**Output:** Single self-contained HTML report (`docs/index.html`) with interactive Plotly charts, generated from a papermill notebook pipeline.

---

## Architecture

### Source modules (`src/`)

| Module | Responsibility |
|--------|---------------|
| `src/usa_data.py` | Embedded BLS OES 2023 salary + employment data; `get_merged_usa_data()` |
| `src/india_data.py` | Embedded NASSCOM/MOSPI 2023 data; `get_merged_india_data()` |
| `src/china_data.py` | Embedded NBS 2023 sector wage data; `get_merged_china_data()` |
| `src/ppp_data.py` | IMF 2023 PPP conversion factors (USD per local currency unit); used by all three country modules |

Each country module exposes a single `get_merged_*_data()` → `pd.DataFrame` with a common schema (see below), and writes `data/processed/merged_*_data.csv` when run as a notebook.

### Common schema

Every merged CSV shares these columns (where available per country):

| Column | Type | Description |
|--------|------|-------------|
| `role` | str | Standardized role name (e.g. `software_engineer`, `lawyer`) |
| `sector` | str | Industry sector (e.g. `tech`, `healthcare`, `agriculture`) |
| `career_stage` | str | `entry`, `mid`, `senior` |
| `median_salary_local` | float | Median annual salary in local currency |
| `median_salary_ppp_usd` | float | PPP-adjusted USD equivalent |
| `employed_thousands` | float | Estimated headcount (thousands) |
| `yoy_wage_growth_pct` | float | Year-over-year wage growth % (latest year) |
| `wage_2019` / `wage_2020` / ... / `wage_2023` | float | Local-currency median wage per year (growth series) |
| `employment_2019` / ... / `employment_2023` | float | Headcount (thousands) per year |
| `country` | str | `USA`, `India`, `China` |

### Directory layout

```
software-stats/
├── src/
│   ├── usa_data.py
│   ├── india_data.py
│   ├── china_data.py
│   └── ppp_data.py
├── data/
│   ├── raw/
│   │   ├── fetch_bls_oes.py          # provenance doc: BLS OES download
│   │   ├── fetch_india_nasscom.py    # provenance doc: NASSCOM reports
│   │   └── fetch_china_nbs.py        # provenance doc: NBS sector wages
│   └── processed/
│       ├── merged_usa_data.csv
│       ├── merged_india_data.csv
│       └── merged_china_data.csv
├── notebooks/                        # 20 notebooks, run in order
├── scripts/
│   └── generate_html.py              # extracts Plotly outputs → docs/index.html
├── docs/
│   └── index.html
├── pyproject.toml
└── CLAUDE.md
```

---

## Notebook Pipeline (20 notebooks)

Run in order within each section; Section 1 must complete before any other section.

### Section 1 — Data Collection (run first)

| # | Notebook | Output CSV |
|---|----------|-----------|
| 01 | `01_usa_data_collection` | `merged_usa_data.csv` |
| 02 | `02_india_data_collection` | `merged_india_data.csv` |
| 03 | `03_china_data_collection` | `merged_china_data.csv` |

### Section 2 — Pay Comparisons

| # | Notebook | Charts |
|---|----------|--------|
| 04 | `04_usa_pay` | Bar: SWE vs lawyer/doctor/nurse/analyst/construction/farmworker at entry/mid/senior (USD) |
| 05 | `05_india_pay` | Same roles, India (INR + PPP-USD overlay) |
| 06 | `06_china_pay` | Same roles, China (CNY + PPP-USD overlay) |
| 07 | `07_pay_cross_country` | Grouped bar: SWE PPP-USD by country at each career stage; scatter: SWE pay vs country GDP/capita |

### Section 3 — Job Volume

| # | Notebook | Charts |
|---|----------|--------|
| 08 | `08_usa_volume` | Bar: total employed by role (USA); pie: tech workforce share of total |
| 09 | `09_india_volume` | Same, India |
| 10 | `10_china_volume` | Same, China |
| 11 | `11_volume_cross_country` | Stacked bar: tech workforce as % of total employed across countries; bubble: pay vs headcount |

### Section 4 — Growth Trends

| # | Notebook | Charts |
|---|----------|--------|
| 12 | `12_usa_growth` | Line: wage growth 2019–2023 by role (USA); line: employment growth by role |
| 13 | `13_india_growth` | Same, India |
| 14 | `14_china_growth` | Same, China |
| 15 | `15_growth_cross_country` | Line: SWE wage growth convergence/divergence across countries; heatmap: growth rate by role × country |

### Section 5 — SWE vs the World

| # | Notebook | Charts |
|---|----------|--------|
| 16 | `16_swe_vs_peers_usa` | Bar: SWE pay multiple over median, blue-collar, and professional peers (USA) |
| 17 | `17_swe_vs_peers_india` | Same, India |
| 18 | `18_swe_vs_peers_china` | Same, China |
| 19 | `19_swe_vs_world_summary` | Grouped bar: SWE relative advantage by country; scatter: SWE-to-median-wage ratio vs country |
| 20 | `20_purchasing_power` | Bar: what SWE salary buys (Big Mac index, rent, local median income multiple) per country |

---

## Roles Covered

| Role | Sector | Education proxy |
|------|--------|-----------------|
| Software Engineer | Tech | Bachelor's (CS/Eng) |
| Lawyer | Legal | Graduate (JD/LLB) |
| Physician | Healthcare | Graduate (MD/MBBS) |
| Financial Analyst | Finance | Bachelor's (Finance) |
| Registered Nurse | Healthcare | Bachelor's/diploma |
| Civil/Mechanical Engineer | Engineering | Bachelor's |
| Construction Laborer | Blue-collar | No degree |
| Farm Worker | Agriculture | No degree |
| Manufacturing Worker | Manufacturing | No degree |
| Retail/Service Worker | Services | No degree |

---

## Data Sources

| Dataset | Source | Country | Vintage |
|---------|--------|---------|---------|
| Occupational Employment & Wage Statistics | BLS OES | USA | 2023 |
| IT sector employment & salaries | NASSCOM Annual Report | India | 2023 |
| Employment survey by sector | MOSPI PLFS | India | 2022–23 |
| Average wages by sector | China NBS Statistical Yearbook | China | 2023 |
| PPP conversion factors | IMF WEO / World Bank | All | 2023 |
| Cost-of-living proxies | Numbeo / Big Mac index | All | 2023 |

All data embedded as Python dicts — no API keys or downloads required at runtime. `data/raw/fetch_*.py` files document original sources and how to refresh.

---

## Running the Pipeline

```bash
# Setup
uv venv && uv pip install -e .

# Section 1 (required first)
for nb in notebooks/0{1..3}_*.ipynb; do
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

# Sections 2–5 (can run in any order after section 1)
for nb in notebooks/{04..20}_*.ipynb; do
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

# Generate report
.venv/bin/python scripts/generate_html.py
```

---

## Dependencies

Identical to homelessness-stats:
```
pandas, numpy, plotly, scipy, statsmodels, papermill, nbconvert, jupyter, requests, python-dotenv
```
Python 3.9+, managed with `uv`.
