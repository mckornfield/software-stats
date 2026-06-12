"""
Fetch USA BLS OES (Occupational Employment and Wage Statistics) data.

Source: U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics
  URL: https://www.bls.gov/oes/current/oes_nat.htm
  Direct download: https://www.bls.gov/oes/special.requests/oesm23nat.zip

The embedded _USA_SALARIES and _USA_GROWTH dicts in src/usa_data.py contain
May 2023 median wages and employment for the SOC codes below.

SOC codes used:
  15-1252  Software Developers  (median $130,160; employed 1,825K)
  23-1011  Lawyers              (median $145,760; employed 698K)
  29-1210x Physicians & Surgeons(median $229,300; employed 748K)
  13-2051  Financial Analysts   (median $99,890;  employed 333K)
  29-1141  Registered Nurses    (median $81,220;  employed 3,238K)
  17-2051  Civil Engineers      (median $95,890;  employed 338K)
  47-2061  Construction Laborers(median $44,850;  employed 1,434K)
  45-2092  Farmworkers & Laborers(median $35,020; employed 800K)
  51-XXXX  Production Workers   (median $45,040;  employed 9,000K)
  41-2031  Retail Salespersons  (median $36,530;  employed 4,186K)

To refresh:
  1. Download and unzip oesm23nat.zip
  2. Open all_data_M_2023.xlsx
  3. Filter by SOC code, read annual_mean and tot_emp columns
  4. Update _USA_SALARIES and _USA_GROWTH in src/usa_data.py
"""
