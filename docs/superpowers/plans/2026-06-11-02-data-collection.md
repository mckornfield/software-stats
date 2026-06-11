# Software-Stats Data Collection Notebooks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and execute notebooks 01–03 that call the src/ data modules and write the three processed CSVs that all analysis notebooks depend on.

**Architecture:** Each notebook imports its country module via a `sys.path` insert pointing to `../src`, calls `get_merged_*_data()`, prints a summary, and writes `data/processed/merged_*_data.csv`. Notebooks are executed with papermill (`--cwd notebooks`).

**Tech Stack:** Python 3.9+, pandas, papermill, nbformat

**Prerequisites:** Scaffold plan complete — `src/usa_data.py`, `src/india_data.py`, `src/china_data.py`, `src/ppp_data.py` exist and tests pass.

**Repo location:** `/Users/mckornfield/repo/homelessness-stats/software-stats`

---

### Task 1: USA data collection notebook

**Files:**
- Create: `notebooks/01_usa_data_collection.ipynb`

- [ ] **Step 1: Create the notebook**

Create `notebooks/01_usa_data_collection.ipynb` with this exact content (valid nbformat 4 JSON):

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": "# USA Data Collection\n\nLoads embedded BLS OES 2023 data from `src/usa_data.py` and writes `data/processed/merged_usa_data.csv`."
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "import sys\nfrom pathlib import Path\nROOT = Path().resolve().parent\nsys.path.insert(0, str(ROOT / 'src'))\n\nimport pandas as pd\nfrom usa_data import get_merged_usa_data"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "df = get_merged_usa_data()\nprint(f'USA data: {len(df)} rows, {len(df.columns)} columns')\nprint(f'Roles: {sorted(df[\"role\"].unique())}')\nprint(f'Career stages: {sorted(df[\"career_stage\"].unique())}')\ndf.head()"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "out = ROOT / 'data' / 'processed' / 'merged_usa_data.csv'\ndf.to_csv(out, index=False)\nprint(f'Wrote {len(df)} rows to {out}')\nprint(df.columns.tolist())"
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.9.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

- [ ] **Step 2: Execute the notebook with papermill**

```bash
cd /Users/mckornfield/repo/homelessness-stats/software-stats
.venv/bin/python -m papermill notebooks/01_usa_data_collection.ipynb notebooks/01_usa_data_collection.ipynb --cwd notebooks
```

Expected: notebook executes cleanly, no exceptions.

- [ ] **Step 3: Verify CSV output**

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/merged_usa_data.csv')
print(f'Shape: {df.shape}')
print(df.columns.tolist())
print(df[['role','career_stage','median_salary_local','median_salary_ppp_usd']].head(6))
"
```

Expected: 30 rows (10 roles × 3 career stages), columns include `median_salary_ppp_usd`, `wage_2019`–`wage_2023`.

- [ ] **Step 4: Commit**

```bash
git add notebooks/01_usa_data_collection.ipynb data/processed/merged_usa_data.csv
git commit -m "feat: add USA data collection notebook and processed CSV"
```

---

### Task 2: India data collection notebook

**Files:**
- Create: `notebooks/02_india_data_collection.ipynb`

- [ ] **Step 1: Create the notebook**

Create `notebooks/02_india_data_collection.ipynb`:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": "# India Data Collection\n\nLoads embedded NASSCOM/MOSPI 2023 data from `src/india_data.py` and writes `data/processed/merged_india_data.csv`."
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "import sys\nfrom pathlib import Path\nROOT = Path().resolve().parent\nsys.path.insert(0, str(ROOT / 'src'))\n\nimport pandas as pd\nfrom india_data import get_merged_india_data"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "df = get_merged_india_data()\nprint(f'India data: {len(df)} rows, {len(df.columns)} columns')\nprint(f'Roles: {sorted(df[\"role\"].unique())}')\nprint(f'SWE mid salary (INR): {df[(df.role==\"software_engineer\")&(df.career_stage==\"mid\")][\"median_salary_local\"].values[0]:,}')\nprint(f'SWE mid salary (PPP USD): {df[(df.role==\"software_engineer\")&(df.career_stage==\"mid\")][\"median_salary_ppp_usd\"].values[0]:,.0f}')\ndf.head()"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "out = ROOT / 'data' / 'processed' / 'merged_india_data.csv'\ndf.to_csv(out, index=False)\nprint(f'Wrote {len(df)} rows to {out}')"
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.9.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

- [ ] **Step 2: Execute**

```bash
.venv/bin/python -m papermill notebooks/02_india_data_collection.ipynb notebooks/02_india_data_collection.ipynb --cwd notebooks
```

Expected: completes cleanly. Output includes `SWE mid salary (INR): 1,200,000` and `SWE mid salary (PPP USD): 54,545`.

- [ ] **Step 3: Verify CSV**

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/merged_india_data.csv')
print(f'Shape: {df.shape}')
print(df[['role','career_stage','median_salary_local','median_salary_ppp_usd']].head(6))
"
```

Expected: 30 rows, INR salaries in hundreds of thousands, PPP USD in tens of thousands.

- [ ] **Step 4: Commit**

```bash
git add notebooks/02_india_data_collection.ipynb data/processed/merged_india_data.csv
git commit -m "feat: add India data collection notebook and processed CSV"
```

---

### Task 3: China data collection notebook

**Files:**
- Create: `notebooks/03_china_data_collection.ipynb`

- [ ] **Step 1: Create the notebook**

Create `notebooks/03_china_data_collection.ipynb`:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": "# China Data Collection\n\nLoads embedded NBS 2023 data from `src/china_data.py` and writes `data/processed/merged_china_data.csv`."
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "import sys\nfrom pathlib import Path\nROOT = Path().resolve().parent\nsys.path.insert(0, str(ROOT / 'src'))\n\nimport pandas as pd\nfrom china_data import get_merged_china_data"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "df = get_merged_china_data()\nprint(f'China data: {len(df)} rows, {len(df.columns)} columns')\nprint(f'Roles: {sorted(df[\"role\"].unique())}')\nprint(f'SWE mid salary (CNY): {df[(df.role==\"software_engineer\")&(df.career_stage==\"mid\")][\"median_salary_local\"].values[0]:,}')\nprint(f'SWE mid salary (PPP USD): {df[(df.role==\"software_engineer\")&(df.career_stage==\"mid\")][\"median_salary_ppp_usd\"].values[0]:,.0f}')\ndf.head()"
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": "out = ROOT / 'data' / 'processed' / 'merged_china_data.csv'\ndf.to_csv(out, index=False)\nprint(f'Wrote {len(df)} rows to {out}')"
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.9.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

- [ ] **Step 2: Execute**

```bash
.venv/bin/python -m papermill notebooks/03_china_data_collection.ipynb notebooks/03_china_data_collection.ipynb --cwd notebooks
```

Expected: completes cleanly. Output includes `SWE mid salary (CNY): 200,000` and `SWE mid salary (PPP USD): 48,780`.

- [ ] **Step 3: Verify CSV**

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/merged_china_data.csv')
print(f'Shape: {df.shape}')
print(df[['role','career_stage','median_salary_local','median_salary_ppp_usd']].head(6))
"
```

Expected: 30 rows.

- [ ] **Step 4: Commit**

```bash
git add notebooks/03_china_data_collection.ipynb data/processed/merged_china_data.csv
git commit -m "feat: add China data collection notebook and processed CSV"
```
