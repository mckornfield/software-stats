"""
Fetch India IT/job market salary data.

Primary sources:
  NASSCOM Strategic Review 2023 (annual IT sector report)
    URL: https://nasscom.in/knowledge-center/publications/
    Key stats: ~5.43M employees in IT-BPM, average salary ~₹1.2M/year

  MOSPI Periodic Labour Force Survey (PLFS) 2022-23
    URL: https://mospi.gov.in/plfs-annual-report
    Key stats: employment by sector, weekly earnings by occupation

  Salary data for non-IT roles sourced from:
    - PayScale India Salary Report 2023: https://www.payscale.com/research/IN/
    - ASSOCHAM Healthcare Salary Survey 2023
    - Bar Council of India statistics

To refresh:
  Update _INDIA_SALARIES and _INDIA_GROWTH in src/india_data.py
  PPP factor for India (22.0 INR/PPP USD) from IMF WEO 2023:
    https://www.imf.org/en/Publications/WEO/weo-database/2023/April
"""
