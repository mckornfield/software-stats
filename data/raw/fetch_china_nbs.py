"""
Fetch China NBS (National Bureau of Statistics) sector wage data.

Primary sources:
  NBS Statistical Yearbook 2023 (中国统计年鉴2023)
    URL: https://www.stats.gov.cn/sj/ndsj/2023/indexeh.htm
    Table: Average Wages of Employed Persons by Sector
    IT sector (Information Transmission, Software and IT Services): ¥201,506/year

  NBS Data Explorer (online query tool)
    URL: https://data.stats.gov.cn/
    Series: A0B0C (average wages by industry)

  Additional sources:
    - MIIT (Ministry of Industry and IT) sector employment data
    - Zhaopin/Boss Zhipin published salary reports for role-level breakdowns
    - ILO China Labour Market country brief 2023

To refresh:
  Update _CHINA_SALARIES and _CHINA_GROWTH in src/china_data.py
  PPP factor for China (4.1 CNY/PPP USD) from IMF WEO 2023:
    https://www.imf.org/en/Publications/WEO/weo-database/2023/April
"""
