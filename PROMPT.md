# Lab 4 — Prompt used with Claude (Student Inputs)

> Generate the Python code, requirements file, and all additional assets necessary to deploy my dashboard, using the information provided below.

| Field | Input |
|---|---|
| **Company Name** | Wolf & Badger Ltd |
| **Industry / Sector** | Online marketplace for independent fashion & lifestyle brands (e-commerce + 3 stores in London, New York, Los Angeles); UK, private, Certified B Corp |
| **Audience** | Sustainability analysts who monitor, analyse and report ESG metrics across the organisation |
| **Purpose of Dashboard** | The analyses and recommendations inform the Sustainability Director, who communicates key findings, risks and progress to the Board of Directors |
| **Time horizon** | FY2021–2035 (actuals FY2021–FY2025 where available; scenario projections to 2035) |
| **Key ESG Questions** | (1) Is the footprint growing faster than the business? (2) What drives emissions, and how much of the change is real vs methodological? (3) Can W&B hit a credible 2030 Scope 3 target while growing ~15% a year? (4) Where are the disclosure gaps? (5) Are social and governance practices improving? |
| **Environmental Metrics** | Scope 1, Scope 2 (location & market), Scope 3 total and by category, emissions intensity (t/£m GMV), freight data method (activity vs spend), electricity (modelled), renewable share, water & waste (disclosure gaps) |
| **Social Metrics** | Employee engagement score, women in leadership, headcount (derived), brands approved under the Happy Worker Guarantee, brands vetted |
| **Governance Metrics** | B Impact Assessment scores (overall and by area, 2021 vs 2025), independent non-executives, Remuneration Committee, gender pay gap publication, third-party assurance |
| **Target or goal tracking** | Illustrative 2030 Scope 3 reduction (adjustable; company target not yet set); BAU vs decarbonisation scenarios to 2035; required annual intensity reduction |
| **Data Sources** | W&B Annual Impact Reports 2024 & 2025; B Corp Impact Report 2023; B Lab public directory; Lab 1 data-quality inventory — CSVs in `data/` |
| **Desired Visualizations** | KPI tiles, stacked bars by scope and category, dual-axis absolute vs intensity, waterfall bridge (restatement + drivers), scenario line chart with sliders, gauge, grouped bars, funnel, quality-score bar chart, recommendation table |
| **Style** | Clean, light, earthy greens; clear labels for estimated and modelled values |

## Decisions the dashboard supports
- Whether to prioritise freight data quality before setting a Scope 3 target
- What level of intensity reduction a 2030 target implies at the planned growth rate
- Which disclosure gaps to close in the next impact report

## Story the data tells
Social and governance performance is improving and verified (B Impact score 81 → 108.8), but the climate footprint
is almost entirely freight and is rising with sales (+55% reported, ~+15% like-for-like). There is no quantified
target and no assurance.

## Areas requiring urgent attention
Scope 3 freight growth, freight data quality, missing energy/water/waste data, and the lack of assurance and board
disclosure.
