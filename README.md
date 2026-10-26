# B Corp Benchmark & Impact Tracker — ADJOAA × Wolf & Badger

Live app: https://wolf-badger-esg-dashboard.streamlit.app/

A Streamlit dashboard for **ADJOAA** (a curated online marketplace for African and Black-owned designers) to track its
impact KPIs each quarter and year, and to make decisions on its B Corp journey. It benchmarks against
**Wolf & Badger**, a UK marketplace for independent brands that has been a Certified B Corp since 2021
(B Impact score 81.0 → 108.8, verified by B Lab).

> Independent analysis of public reports for internal planning. Not produced by or affiliated with Wolf & Badger or B Lab.

## What's inside
| Tab | Use it to… |
|---|---|
| 🧭 Overview | See ADJOAA's scorecard status, W&B headline numbers, and five lessons from the benchmark |
| 🏅 B Corp journey (benchmark) | Follow what W&B disclosed each year (2021–2025) and where its B Impact points came from |
| 📋 ADJOAA tracker | Edit KPI values and targets; status (Met / Improving / Not measured…) updates automatically |
| 🎯 B Impact readiness | Enter ADJOAA's self-assessed B Impact scores and compare them with W&B and the 80-point threshold |
| 🌍 Climate & scenarios | W&B's footprint as a benchmark plus a growth-vs-emissions calculator for ADJOAA |
| 🔎 Data & methods | Sources, data quality, limitations |

## Updating the data (quarterly / annually)
**Option A — in the app (no coding):**
1. Open **ADJOAA tracker** and edit `current value`, `current_period`, `target` and `owner` in the table.
2. Click **Download updated tracker**.
3. On GitHub: open the `data` folder → **Add file → Upload files** → drop `adjoaa_kpi_tracker.csv` → **Commit changes**.
   The app redeploys automatically within about a minute.

**Option B — directly on GitHub:** open `data/adjoaa_kpi_tracker.csv` → ✏️ (Edit) → change the values → **Commit changes**.

Suggested cadence: **quarterly** for brand vetting, shipping data, packaging and returns; **annually** for the
carbon footprint, team metrics, B Impact self-assessment and the impact report.

## Data files (`data/`)
| File | Content |
|---|---|
| `adjoaa_kpi_tracker.csv` | ADJOAA KPI scorecard (21 KPIs, editable): baseline, current, target, owner, W&B benchmark |
| `adjoaa_bia_readiness.csv` | ADJOAA self-assessed B Impact scores by area vs W&B 2021/2025 |
| `wb_disclosure_timeline.csv` | What W&B disclosed and which targets it stated each year, 2021–2025 |
| `emissions_annual.csv`, `scope3_categories.csv` | W&B GHG data FY2023 (original & restated) and FY2024 |
| `b_impact_scores.csv` | W&B B Impact Assessment by area, 2021 vs 2025 |
| `social_governance.csv` | W&B social & governance metrics |
| `kpi_quality_lab1.csv` | Disclosure-quality scores for 41 W&B KPIs |

**Sources:** W&B Sustainability Report 2022 (summary), B Corp Impact Report 2023, Annual Impact Reports 2024 & 2025,
B Lab public directory. ADJOAA public figures from adjoaa.com and the ICT Pulse interview (Sep 2025).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
- W&B figures are self-reported and not third-party assured. FY2023 emissions were restated (7,619 → 6,650 t).
- W&B's 2025 B Impact area scores are read from a report chart (overall and Governance confirmed by B Lab).
- In-app edits are temporary until the downloaded CSV is committed to GitHub.
- Scenario projections are what-if tools, not forecasts.
- B Lab introduced new standards in 2025; confirm which version applies to ADJOAA's certification timeline.

Originally developed for SAM 503 (ESG Analytics & Management), IIT Stuart School of Business — see `PROMPT.md` and `notebooks/`.
