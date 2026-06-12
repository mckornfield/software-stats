#!/bin/bash
set -e
cd /Users/mckornfield/repo/homelessness-stats/software-stats

# Step 1: Create venv
uv venv --quiet
echo "venv created"

# Step 2: Install deps
uv pip install -e . -q
echo "deps installed"

# Step 3: Install pytest (not in pyproject.toml but needed for tests)
uv pip install pytest -q
echo "pytest installed"

# Step 4: Run tests
.venv/bin/python -m pytest tests/ -v
echo "tests done"

# Step 5: Run data collection notebooks
for nb in notebooks/01_usa_data_collection.ipynb notebooks/02_india_data_collection.ipynb notebooks/03_china_data_collection.ipynb; do
  echo "Running $nb..."
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

# Step 6: Run analysis notebooks 04-20
for nb in notebooks/04_usa_pay.ipynb notebooks/05_india_pay.ipynb notebooks/06_china_pay.ipynb notebooks/07_pay_cross_country.ipynb notebooks/08_usa_volume.ipynb notebooks/09_india_volume.ipynb notebooks/10_china_volume.ipynb notebooks/11_volume_cross_country.ipynb notebooks/12_usa_growth.ipynb notebooks/13_india_growth.ipynb notebooks/14_china_growth.ipynb notebooks/15_growth_cross_country.ipynb notebooks/16_swe_vs_peers_usa.ipynb notebooks/17_swe_vs_peers_india.ipynb notebooks/18_swe_vs_peers_china.ipynb notebooks/19_swe_vs_world_summary.ipynb notebooks/20_purchasing_power.ipynb; do
  echo "Running $nb..."
  .venv/bin/python -m papermill "$nb" "$nb" --cwd notebooks
done

echo "All notebooks done"

# Step 7: Generate HTML report
.venv/bin/python scripts/generate_html.py

echo "HTML report generated"
