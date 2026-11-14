# India’s Vehicle Registrations in 2025 | VAHAN

> **What changed when vehicle registrations more than doubled in a month?**

October stood out as soon as I plotted the year: recorded registrations went from **1.93 million in September to 4.17 million in October**. The total told me how big the jump was. I wanted to know where it came from within the data, and whether the manufacturers growing fastest were also gaining share.

**29.29 million registrations** · **12 monthly exports** · **3 Tableau dashboards**

[**Open the interactive Tableau workbook ↗**](https://public.tableau.com/app/profile/bhavya.rajyaguru/viz/IndiaVehicleRegistrations2025/FuelMixandChange) · [Findings](#what-i-found) · [Dashboard tour](#tableau-dashboard-tour) · [Reproduce the analysis](#reproduce-the-analysis)

**Bhavya Rajyaguru** · Independent portfolio project · Excel, Python, SQL and Tableau Public

## What I found

### 1. What does the quarterly total hide?

October was the busiest month in the selected VAHAN exports, with **4,170,511 registrations**, up **116.0%** from September. The fourth quarter reached **9.77 million**, up **61.2%** from Q3. The quarterly figure hides the reversal within those three months: registrations fell to **3.45 million in November** and **2.15 million in December**. December alone was down **37.8%** from November. PETROL registrations fell by **954,051** in that comparison; Hero MotoCorp had the largest decline among manufacturer labels (**599,239**).

![Monthly VAHAN registration totals for 2025, with October highlighted](assets/monthly-trend.png)

### 2. Which fuels and manufacturers accounted for the jump?

| Fuel label as reported by VAHAN | Extra registrations, September to October | Share of net increase |
| --- | ---: | ---: |
| PETROL | +1,303,963 | 58.2% |
| PETROL(E20) | +687,160 | 30.7% |
| All other fuel labels combined | +248,303 | 11.1% |
| **Net increase** | **+2,239,426** | **100.0%** |

Start with the first two rows: **PETROL and PETROL(E20) together accounted for 88.9% of the increase.** That still leaves some movement worth looking at. DIESEL added **96,369** registrations, while LPG ONLY fell by **1,857**. The largest manufacturer contributions were **Hero MotoCorp (+676,288)**, **Honda Motorcycle and Scooter India (+511,346)** and **TVS Motor (+317,124)**. The fuel and manufacturer figures describe the same increase from two angles.

The fuel mix also changed over the year. PETROL went from **69.62%** of January registrations to **24.43%** in December. PETROL(E20) went from **2.53%** to **45.03%**. Their full-year shares were **54.35%** and **20.59%**, respectively. This tells us how the reported mix changed; the data does not track whether individual buyers switched fuels.

### 3. How can registrations rise while market share falls?

Suzuki Motorcycle India was the clearest example I found. Its registration count grew **72.4%**: it registered **82,448 vehicles in September** and **142,140 in October**. Its share fell from **4.27% to 3.41%** because total registrations grew faster. This is why I compare volume, growth and share change separately.

I also checked how concentrated registrations were. The ten largest manufacturers in each month accounted for **81.11%** of September registrations, **87.59%** in October and **77.68%** in December. Across the full year, **Hero MotoCorp** ranked first with **5.93 million registrations (20.24%)**, followed by Honda Motorcycle and Scooter India and TVS Motor.

I also wanted to know how much the rankings depended on including smaller manufacturers. I reran them with minimum September counts of **100, 1,000 and 10,000**. Hero MotoCorp and Honda stayed first and second, while TVS moved from sixth to third as the cutoff rose. Raising the cutoff changes who qualifies for the ranking; each manufacturer’s share is still calculated against the full market total for that month.

![Growth and share change for Suzuki Motorcycle India and Hero MotoCorp](assets/growth-vs-share.png)

## Tableau dashboard tour

[![Fuel Mix and Change dashboard showing monthly fuel shares, a growth heatmap and October contribution charts](assets/fuel-mix-and-change.png)](https://public.tableau.com/app/profile/bhavya.rajyaguru/viz/IndiaVehicleRegistrations2025/FuelMixandChange)

**If you only have a minute, start with the October waterfall.** It shows how the two petrol labels and all other fuels add up to the **2.24 million** net increase. From there, use the workbook tabs to explore the three views:

1. **Registration Overview:** See the annual total, the monthly trend and the top ten manufacturers by full-year registrations. Compare that ranking with the October contribution chart to see who led for the year and who added the most in one month.
2. **Manufacturer Explorer:** Read registration growth and share change on the same scatter plot. Adjust the minimum September count and see which names remain. Hover over a manufacturer for the exact values. The two-manufacturer chart above is a static illustration; the full comparison is in Tableau.
3. **Fuel Mix and Change:** Read the year’s fuel mix in the 100% stacked bars and see month-to-month movements in the heatmap. Hover over the October waterfall for exact fuel contributions, then compare with the top ten manufacturer contributions alongside it.

## From monthly exports to a dashboard I could check

I reviewed the 12 VAHAN Maker and Fuel Data exports and used the dates inside each report to select January–December 2025. One detail mattered before I could chart anything: some filenames contain “2026,” even though the reports cover 2025. I used the reporting dates inside the files. The [input manifest](monthly_checks.csv) records the selected source file and registration total for each month, including the replacement October and November exports.

In Python, I turned fuel columns into rows. The working file contains **301,433 aggregate rows**, **2,046 manufacturer labels** and **25 fuel labels**. Each row is one month, manufacturer and reported fuel label, with a registration count and source filename. I kept VAHAN’s labels, including separate PURE EV and ELECTRIC(BOV) categories.

I checked for duplicate keys, missing fields, negative counts and missing months. I matched manufacturer totals back to the source reports, matched monthly totals to the manifest, and verified that fuel and manufacturer contributions each added up to the recorded monthly change. I then used SQL to cross-check monthly growth, annual fuel shares, September-to-October manufacturer growth versus share, and October fuel contributions. The SQL queries were checked in SQLite; the MySQL 8 setup and import were not tested on a MySQL server.

<details>
<summary><strong>How the metrics are calculated</strong></summary>

- **Registrations:** Sum the counts. The number of rows is not the number of vehicles.
- **Growth:** Divide the change by the previous period’s count. Growth is blank if the previous count is zero or unavailable. January has no preceding month in the dataset.
- **Share:** Divide group registrations by total registrations for the same period. For a manufacturer’s own fuel mix, use that manufacturer’s total as the denominator.
- **Share change:** Subtract the September share from the October share and report the difference in percentage points.
- **Concentration:** Add the shares of the five or ten largest manufacturers in each month.
- **Contribution:** Subtract previous registrations from current registrations and retain negative moves. If a label is missing in one export, treat it as having no *recorded* volume on that side for reconciliation. Mark it with a coverage flag and leave matched growth and share comparisons blank.

</details>

## Reproduce the analysis

With **Python 3.10+**, run this from the project folder. No third-party packages are needed.

```bash
python3 analyse.py
```

This uses the included [prepared data](vahan_2025_working.csv.gz) and [monthly checks](monthly_checks.csv) to regenerate the summaries. If you have the original reports, run `python3 prepare_data.py /path/to/exports` first. The original reports are not included. Python reads the compressed CSV directly. To load it in a database, extract it first with `gunzip -k vahan_2025_working.csv.gz` or a gzip utility.

- **Scripts:** [prepare_data.py](prepare_data.py) reshapes the reports; [analyse.py](analyse.py) validates the combined file and generates the summaries.
- **Monthly and quarterly trends:** [monthly_growth.csv](monthly_growth.csv) · [quarterly_growth.csv](quarterly_growth.csv)
- **Annual rankings and concentration:** [maker_annual.csv](maker_annual.csv) · [fuel_annual.csv](fuel_annual.csv) · [concentration.csv](concentration.csv)
- **Monthly breakdowns and cutoffs:** [maker_movement.csv](maker_movement.csv) · [fuel_movement.csv](fuel_movement.csv) · [maker_fuel_mix.csv](maker_fuel_mix.csv) · [growth_rank_sensitivity.csv](growth_rank_sensitivity.csv)
- **SQL:** [Table schema](sql/01_schema.sql) · [Analysis queries](sql/02_market_analysis.sql). The queries use CTEs, window functions, a join across months and conditional aggregation.

## Did October stand out in another report?

Yes. FADA’s published series also more than doubled from September to October. In that series, **two-wheelers accounted for 84.8% of the net increase**. FADA also draws on registration data, so I used it to compare the direction and scale of the jump across publications. The [evidence notes](docs/evidence.md) show the figures side by side and break down which manufacturers led each petrol label’s increase.

## What the results tell us

The clearest finding is where October’s increase showed up: two reported fuel labels made up nearly nine-tenths of the net change, and FADA’s series points to two-wheelers as the largest contributor in its own breakdown. The VAHAN totals reconcile within the selected reports. I did not independently confirm national coverage or identical filters across months, so I treat these as findings about recorded registrations. To test whether the pattern repeats around the festive period, I’d compare equivalent weeks across years using consistent state and vehicle-class filters.

**Source:** VAHAN Maker and Fuel Data, January–December 2025  
**Author:** Bhavya Rajyaguru · [LinkedIn](https://www.linkedin.com/in/rajyaguru-bhavya) · [Email](mailto:bhavyarajyaguru01@gmail.com)
