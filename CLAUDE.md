# Project: Software Engineering Job Market Analysis

## Overview
Analyzes software engineering pay and employment in the USA, India, and China.
Compares SWE roles against professional peers (lawyer, doctor, nurse, financial analyst)
and blue-collar/agricultural roles. Includes PPP-adjusted cross-country comparisons,
job volume, and 2019–2023 growth trends. Produces interactive Plotly charts and a
single self-contained HTML report.

## Architecture
- `src/usa_data.py`   — Embedded BLS OES 2023 salary + employment + growth data
- `src/india_data.py` — Embedded NASSCOM/MOSPI 2023 data (INR)
- `src/china_data.py` — Embedded NBS 2023 sector wage data (CNY)
- `src/ppp_data.py`   — IMF 2023 PPP + market FX factors; to_ppp_usd / to_usd_nominal
- `src/sector_data.py` — economy-wide employment by sector per country (2023); get_sector_employment(country)
- `data/raw/`         — Provenance-only fetch scripts (no runtime dependency)
- `data/processed/`   — merged_usa_data.csv, merged_india_data.csv, merged_china_data.csv
- `notebooks/`        — 20 notebooks in 5 thematic sections
- `scripts/generate_html.py` → `docs/index.html`

## Notebook Pipeline

### Section 1 — Data Collection (run FIRST, others depend on these CSVs)
- 01_usa_data_collection
- 02_india_data_collection
- 03_china_data_collection

### Section 2 — Pay Comparisons (04–07)
### Section 3 — Job Volume (08–11)
### Section 4 — Growth Trends (12–15)
### Section 5 — SWE vs the World (16–20)

## Running Notebooks
```bash
uv venv && uv pip install -e .

# Section 1 first
for nb in notebooks/0{1..3}_*.ipynb; do
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

# Sections 2-5
for nb in notebooks/{04..20}_*.ipynb; do
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

.venv/bin/python scripts/generate_html.py
```

## Roles Covered
software_engineer, lawyer, physician, financial_analyst, registered_nurse,
civil_engineer, construction_laborer, farm_worker, manufacturing_worker, retail_worker

## Common CSV Schema
role, sector, career_stage, median_salary_local,
median_salary_ppp_usd (local buying power, IMF PPP), median_salary_usd (market FX),
employed_thousands, yoy_wage_growth_pct,
wage_2019..wage_2023, emp_2019..emp_2023, country

## Currency conventions
- `median_salary_usd` — market exchange rate (82.6 INR, 7.08 CNY per USD). "What the paycheck converts to."
- `median_salary_ppp_usd` — PPP-adjusted (22 INR, 4.1 CNY per PPP USD). "Local buying power." Already reflects cost of living.
- Per-country pay charts use market USD; cross-country comparisons use PPP USD. No raw INR/CNY in charts.
- `src/ppp_data.py` exposes `to_usd_nominal()` and `to_ppp_usd()`.
