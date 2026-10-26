"""
B Corp Benchmark & Impact Tracker — ADJOAA × Wolf & Badger

Purpose : help ADJOAA track its own impact KPIs each quarter/year and make decisions on its B Corp journey,
          using Wolf & Badger (a B Lab-verified B Corp marketplace with a similar business model) as the benchmark.
Data    : Wolf & Badger public reports (Sustainability Report 2022, B Corp Impact Report 2023,
          Annual Impact Reports 2024 & 2025), B Lab public directory; ADJOAA tracker CSVs in data/.
Run     : streamlit run app.py
"""
from io import StringIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="B Corp Benchmark & Impact Tracker", page_icon="🌿", layout="wide")

DATA = Path(__file__).parent / "data"
INK, MUTED = "#1F2A24", "#6B7770"
GREEN, SAGE, CLAY, SAND, SKY, RED, GOLD = "#2F6B4F", "#8DB59E", "#C0703F", "#E2C792", "#4F7FA8", "#B54A3A", "#D9A441"
LAYOUT = dict(template="simple_white", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
              margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.18),
              hoverlabel=dict(bgcolor="white"))


@st.cache_data
def load(name):
    return pd.read_csv(DATA / name, dtype=str if name.startswith("adjoaa") else None, keep_default_na=False)


em = load("emissions_annual.csv")
s3 = load("scope3_categories.csv")
bia = load("b_impact_scores.csv")
tl = load("wb_disclosure_timeline.csv")
kq = load("kpi_quality_lab1.csv")
for c in ("scope1_t", "scope2_location_t", "scope2_market_t", "scope3_t", "total_reported_t", "gmv_gbp_m",
          "intensity_t_per_gbp_m"):
    em[c] = pd.to_numeric(em[c], errors="coerce")
latest = em[em.version == "Reported"].iloc[0]
base = em[em.version == "Restated"].iloc[0]
orig = em[em.version.str.startswith("Original")].iloc[0]

# ---- tracker state (editable in-session; persisted by downloading the CSV and committing it to GitHub)
if "tracker_base" not in st.session_state:
    st.session_state.tracker_base = load("adjoaa_kpi_tracker.csv").copy()
if "tracker" not in st.session_state:
    st.session_state.tracker = st.session_state.tracker_base.copy()
if "bia_base" not in st.session_state:
    st.session_state.bia_base = load("adjoaa_bia_readiness.csv").copy()


def num(x):
    return pd.to_numeric(pd.Series([x]).astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce").iloc[0]


def status(r):
    cur, tgt, bl, d = str(r.current_value).strip(), str(r.target_value).strip(), str(r.baseline_value).strip(), r.direction
    if cur == "":
        return "⚪ Not measured"
    if d == "yes":
        return "🟢 Met" if cur.lower() == "yes" else "🔴 Not yet"
    c, t, b = num(cur), num(tgt), num(bl)
    if d == "info" or pd.isna(c):
        return "🔵 Tracking"
    if not pd.isna(t):
        if (d == "higher" and c >= t) or (d == "lower" and c <= t):
            return "🟢 Met"
    if not pd.isna(b):
        better = c > b if d == "higher" else c < b
        return "🟡 Improving" if better else "🔴 Off track"
    return "🔵 Tracking" if pd.isna(t) else "🟡 Below target"


def scored(df):
    out = df.copy()
    out.insert(2, "status", out.apply(status, axis=1))
    return out


def pct(a, b):
    return (a - b) / b


st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
div[data-testid="stMetricValue"] {font-size: 1.6rem;}
.callout {border-left: 4px solid #2F6B4F; background: #F3F7F4; padding: .7rem 1rem; border-radius: 4px; margin: .45rem 0;}
.warn {border-left-color: #C0703F; background: #FBF4EE;}
.gap {border: 1px dashed #B54A3A; border-radius: 6px; padding: .8rem; text-align: center; color: #B54A3A;}
.small {color: #6B7770; font-size: .85rem;}
</style>""", unsafe_allow_html=True)

# ============================================================================= sidebar
with st.sidebar:
    st.markdown("### 🌿 B Corp Benchmark & Impact Tracker")
    st.markdown("**Tracked company:** ADJOAA — curated marketplace for African & Black-owned designers")
    st.markdown("**Benchmark:** Wolf & Badger — UK marketplace for independent brands, Certified B Corp since 2021 "
                "(B Impact score 108.8, verified by B Lab)")
    st.divider()
    st.markdown("**Update cycle**")
    st.caption("Quarterly: brand vetting, shipping data, packaging, returns · Annually: footprint, team, impact report")
    st.divider()
    st.markdown("**Download data**")
    for f in sorted(DATA.glob("*.csv")):
        st.download_button(f"⬇ {f.name}", f.read_bytes(), file_name=f.name, mime="text/csv", width="stretch")
    st.caption("Independent analysis of public reports. Not produced by or affiliated with Wolf & Badger. "
               "W&B figures are self-reported and unassured unless noted.")

st.title("B Corp Benchmark & Impact Tracker")
st.caption("ADJOAA's impact KPIs, tracked against the journey of a verified B Corp marketplace (Wolf & Badger, 2021–2025)")

with st.expander("ℹ️ How to use this dashboard (2 minutes)", expanded=False):
    st.markdown("""
1. **Overview**: headline status and the decisions this dashboard supports.
2. **B Corp journey (benchmark)**: what Wolf & Badger disclosed each year, how its B Impact score grew, and the lessons for ADJOAA.
3. **ADJOAA tracker**: the KPI scorecard. **Edit the table directly**, then press *Download updated tracker* to save.
   To make the update permanent for everyone, upload the downloaded file to GitHub as `data/adjoaa_kpi_tracker.csv`.
   The dashboard refreshes within a minute.
4. **B Impact readiness**: enter ADJOAA's self-assessed scores by impact area and compare them with W&B's first certification.
5. **Climate & scenarios**: W&B's footprint as a benchmark, plus a calculator to test ADJOAA growth and target scenarios.
6. **Data & methods**: sources, data quality and limitations.
""")

tabs = st.tabs(["🧭 Overview", "🏅 B Corp journey (benchmark)", "📋 ADJOAA tracker", "🎯 B Impact readiness",
                "🌍 Climate & scenarios", "🔎 Data & methods"])

# ============================================================================= 1. OVERVIEW
with tabs[0]:
    tr = scored(st.session_state.tracker)
    counts = tr.status.value_counts()
    measured = (tr.status != "⚪ Not measured").sum()
    st.subheader("ADJOAA — scorecard snapshot")
    c = st.columns(5)
    c[0].metric("KPIs tracked", len(tr))
    c[1].metric("Measured", f"{measured} / {len(tr)}")
    c[2].metric("🟢 Met", int(counts.get("🟢 Met", 0)))
    c[3].metric("🟡 Improving / below target", int(counts.get("🟡 Improving", 0) + counts.get("🟡 Below target", 0)))
    c[4].metric("🔴 Not yet / off track", int(counts.get("🔴 Not yet", 0) + counts.get("🔴 Off track", 0)))

    st.subheader("Benchmark — Wolf & Badger at a glance")
    c = st.columns(5)
    c[0].metric("B Impact score", "108.8", "+34% vs first cert (81.0)")
    c[1].metric("Years from certification to 108.8", "4", help="May 2021 → June 2025 recertification")
    c[2].metric("Total emissions FY2024", f"{latest.total_reported_t:,.0f} t", f"{pct(latest.total_reported_t, base.total_reported_t):+.0%}",
                delta_color="inverse")
    c[3].metric("Freight share of Scope 3", "78%")
    c[4].metric("Team engagement", "84 / 100", "+13")

    l, r = st.columns([1.1, 1])
    with l:
        st.subheader("Decisions this dashboard supports")
        st.markdown("""
1. **Are we ready to submit for B Corp certification?** → *B Impact readiness*
2. **Which impact KPIs are on track, and which need an owner or budget this quarter?** → *ADJOAA tracker*
3. **What should we measure first, and in what order, to avoid W&B's data problems?** → *B Corp journey*
4. **What would a climate target mean for a fast-growing marketplace?** → *Climate & scenarios*
""")
    with r:
        st.subheader("Five lessons from the benchmark")
        st.markdown("""
<div class="callout"><b>1 · Certify first, then improve.</b> W&B certified with 81.0, just above the 80 threshold, and reached 108.8 four years later.</div>
<div class="callout"><b>2 · Vet every brand.</b> Supply-chain vetting (Guarantees, a mandatory Happy Worker declaration) is the core of a marketplace's impact model.</div>
<div class="callout warn"><b>3 · Measure before you promise.</b> W&B announced "carbon neutral by 2025, net zero by 2030" in 2022, then withdrew to "set realistic targets" once it had data.</div>
<div class="callout warn"><b>4 · Freight is the footprint.</b> 78% of W&B's Scope 3 is delivery. Get carrier activity data from day one: spend-based estimates inflated W&B's trend.</div>
<div class="callout"><b>5 · Publish every year.</b> Annual reports from 2022 onwards built credibility and gave W&B the structure for recertification.</div>
""", unsafe_allow_html=True)

# ============================================================================= 2. B CORP JOURNEY
with tabs[1]:
    st.subheader("What Wolf & Badger disclosed, year by year")
    short = ["Certified B Corp · 81.0", "First sustainability report", "B Corp Impact Report",
             "First GHG inventory published", "Recertified · 108.8"]
    fig = go.Figure()
    fig.add_scatter(x=tl.year.astype(int), y=[1] * len(tl), mode="markers+text+lines", text=short,
                    textposition=["top center", "bottom center"] * 2 + ["top center"],
                    marker=dict(size=18, color=GREEN), line=dict(color=SAGE, width=3),
                    hovertext=tl.what_was_disclosed, hoverinfo="text")
    fig.update_layout(height=170, yaxis=dict(visible=False, range=[0.6, 1.4]), xaxis=dict(dtick=1, range=[2020.5, 2025.5]),
                      showlegend=False, **{k: v for k, v in LAYOUT.items() if k != "legend"})
    st.plotly_chart(fig, width="stretch")
    cols = st.columns(len(tl))
    for col, (_, r) in zip(cols, tl.iterrows()):
        with col:
            st.markdown(f"**{r.year} · {r.milestone}**")
            st.markdown(f"<span class='small'>{r.published}</span>", unsafe_allow_html=True)
            st.markdown(r.what_was_disclosed)
            st.markdown(f"🎯 *Target stated:* {r.climate_target_stated}")
            st.caption(r.source)

    a, b = st.columns([1.2, 1])
    with a:
        areas = ["Governance", "Workers", "Community", "Environment", "Customers"]
        fig = go.Figure()
        for yr, col in (("2021", SAND), ("2025", GREEN)):
            g = bia[(bia.assessment_year.astype(str) == yr) & (bia.impact_area.isin(areas))].set_index("impact_area").loc[areas]
            fig.add_bar(name=f"{yr} ({'first certification' if yr == '2021' else 'recertification'})", x=areas, y=g.score,
                        marker_color=col, text=g.score, textposition="outside")
        fig.update_layout(barmode="group", title="B Impact score by area: where W&B gained 27.8 points", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        st.markdown("#### Where the points came from")
        st.markdown("""
- **Environment +9.6** (+66%): annual GHG measurement and reporting with Greenly.
- **Community +9.2** (+68%): DE&I surveys, paid volunteering, UN Global Compact participation.
- **Workers +4.9**: onboarding, 360° feedback, paid sick leave, an engagement platform.
- **Governance +3.4** (+22%): a Remuneration Committee, ESG KPIs at Board level, a published impact report.
- **Customers +0.8**: still the weakest area. Points come from helping brands improve (the Guarantees).

*2025 area scores are read from the report chart; the overall score (108.8) and Governance (19.0) are confirmed on the B Lab directory.*
""")
    st.info("B Lab published new B Corp standards in 2025 (topic-based requirements instead of a single 80-point threshold). "
            "Confirm with B Lab which version applies to ADJOAA's submission date. The KPIs in the tracker map to both versions.")

# ============================================================================= 3. ADJOAA TRACKER
with tabs[2]:
    st.markdown("Edit **current_value**, **current_period**, **target_value** or **owner** directly in the table. "
                "Status updates automatically. When you finish, **download the updated tracker** and replace "
                "`data/adjoaa_kpi_tracker.csv` on GitHub so the change is saved for everyone.")
    up = st.file_uploader("…or load a previously saved tracker CSV", type="csv")
    if up is not None and st.session_state.get("loaded_file") != up.file_id:
        st.session_state.tracker_base = pd.read_csv(up, dtype=str, keep_default_na=False)
        st.session_state.loaded_file = up.file_id
        st.session_state.ed_ver = st.session_state.get("ed_ver", 0) + 1
    edited = st.data_editor(
        st.session_state.tracker_base, hide_index=True, width="stretch", num_rows="dynamic",
        key=f"tracker_ed_{st.session_state.get('ed_ver', 0)}",
        column_order=["pillar", "kpi", "current_value", "current_period", "target_value", "target_period", "unit",
                      "wb_benchmark", "owner", "frequency", "baseline_value", "baseline_period", "direction", "notes"],
        column_config={
            "pillar": st.column_config.SelectboxColumn(options=["Governance", "Workers", "Community", "Environment", "Customers"]),
            "direction": st.column_config.SelectboxColumn(options=["higher", "lower", "yes", "info"],
                                                          help="higher/lower = which way is better; yes = Yes/No KPI; info = context only"),
            "frequency": st.column_config.SelectboxColumn(options=["Quarterly", "Annual", "One-off"]),
            "kpi": st.column_config.TextColumn("KPI", width="medium"),
            "current_value": st.column_config.TextColumn("✏️ current value"),
            "target_value": st.column_config.TextColumn("✏️ target"),
            "wb_benchmark": st.column_config.TextColumn("W&B benchmark", width="medium"),
        })
    st.session_state.tracker = edited.fillna("").reset_index(drop=True)

    tr = scored(st.session_state.tracker)
    a, b = st.columns([1, 1.3])
    with a:
        order = ["🟢 Met", "🟡 Improving", "🟡 Below target", "🔵 Tracking", "🔴 Not yet", "🔴 Off track", "⚪ Not measured"]
        colors = {"🟢 Met": GREEN, "🟡 Improving": GOLD, "🟡 Below target": SAND, "🔵 Tracking": SKY,
                  "🔴 Not yet": RED, "🔴 Off track": CLAY, "⚪ Not measured": "#C9CFCB"}
        piv = tr.groupby(["pillar", "status"]).size().unstack(fill_value=0)
        fig = go.Figure()
        for s_ in order:
            if s_ in piv:
                fig.add_bar(name=s_, y=piv.index, x=piv[s_], orientation="h", marker_color=colors[s_])
        fig.update_layout(barmode="stack", title="Status by pillar", height=330, **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        st.markdown("#### Next actions (not measured or not yet met)")
        todo = tr[tr.status.isin(["⚪ Not measured", "🔴 Not yet", "🔴 Off track", "🟡 Below target"])][
            ["pillar", "kpi", "status", "owner", "frequency", "target_value", "target_period"]]
        st.dataframe(todo, hide_index=True, width="stretch", height=300)
    st.download_button("⬇ Download updated tracker (adjoaa_kpi_tracker.csv)",
                       st.session_state.tracker.to_csv(index=False).encode(), "adjoaa_kpi_tracker.csv", "text/csv",
                       type="primary")

# ============================================================================= 4. B IMPACT READINESS
with tabs[3]:
    st.markdown("Enter ADJOAA's **self-assessed** score for each impact area from the B Impact Assessment "
                "(bimpactassessment.net). Compare it with Wolf & Badger's first certification (81.0) and the 80-point threshold.")
    br = st.data_editor(st.session_state.bia_base, hide_index=True, width="stretch", key="bia_ed",
                        disabled=["impact_area", "wb_2021_first_cert", "wb_2025_recert"],
                        column_config={"adjoaa_self_assessed": st.column_config.TextColumn("ADJOAA self-assessed (edit)")})
    adj = pd.to_numeric(br.adjoaa_self_assessed, errors="coerce")
    wb21 = pd.to_numeric(br.wb_2021_first_cert)
    wb25 = pd.to_numeric(br.wb_2025_recert)
    a, b = st.columns([1.3, 1])
    with a:
        fig = go.Figure()
        fig.add_bar(name="W&B 2021 (first cert)", x=br.impact_area, y=wb21, marker_color=SAND)
        fig.add_bar(name="W&B 2025", x=br.impact_area, y=wb25, marker_color=SAGE)
        if adj.notna().any():
            fig.add_bar(name="ADJOAA (self-assessed)", x=br.impact_area, y=adj, marker_color=GREEN,
                        text=adj, textposition="outside")
        fig.update_layout(barmode="group", title="Score by impact area", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        total = adj.sum() if adj.notna().any() else None
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta" if total is not None else "gauge",
            value=total if total is not None else 0, delta=dict(reference=80) if total is not None else None,
            title=dict(text="ADJOAA total vs 80 threshold" if total is not None else "Enter scores to see total"),
            gauge=dict(axis=dict(range=[0, 140]), bar=dict(color=GREEN),
                       threshold=dict(line=dict(color=RED, width=4), value=80),
                       steps=[dict(range=[0, 80], color="#F4EDE6"), dict(range=[80, 140], color="#E9F2EC")])))
        fig.update_layout(height=280, margin=dict(l=30, r=30, t=60, b=0))
        st.plotly_chart(fig, width="stretch")
        if total is not None:
            gap = (wb21 - adj).where(adj.notna())
            weakest = br.impact_area[gap.idxmax()] if gap.notna().any() else None
            st.markdown(f"**Gap to W&B's first certification:** {81.0 - total:+.1f} points" +
                        (f" · biggest gap: **{weakest}**" if weakest else ""))
    st.download_button("⬇ Download readiness scores", br.to_csv(index=False).encode(), "adjoaa_bia_readiness.csv", "text/csv")
    st.caption("Under B Lab's 2025 standards, certification moves to topic-based requirements; keep the area scores as an internal readiness gauge.")

# ============================================================================= 5. CLIMATE & SCENARIOS
with tabs[4]:
    st.subheader("Benchmark footprint — Wolf & Badger")
    a, b = st.columns(2)
    with a:
        fig = go.Figure()
        colors3 = {"Freight (Cat. 9 downstream transport)": GREEN, "Digital advertising (Cat. 1)": SAGE,
                   "Service purchases + other (residual)": SAND}
        for cat, g in s3.groupby("category", sort=False):
            fig.add_bar(name=cat, x=g.year.astype(str), y=g.tco2e, marker_color=colors3[cat],
                        text=[f"{v:,.0f}" for v in g.tco2e], textposition="inside")
        fig.update_layout(barmode="stack", title="Scope 3 by category (tCO₂e) — Scope 1 = 0, Scope 2 ≈ 0", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    with b:
        fig = go.Figure()
        fig.add_bar(x=["FY2023", "FY2024"], y=[59, 26], name="Activity-based (carrier data)", marker_color=GREEN,
                    text=["59%", "26%"], textposition="inside")
        fig.add_bar(x=["FY2023", "FY2024"], y=[41, 74], name="Spend-based estimate", marker_color=SAND,
                    text=["41%", "74%"], textposition="inside")
        fig.update_layout(barmode="stack", title="Freight emissions by data method (%)", **LAYOUT)
        st.plotly_chart(fig, width="stretch")
    st.markdown(f"""<div class="callout warn">W&B's total rose <b>{pct(latest.total_reported_t, base.total_reported_t):+.0%}</b>
while GMV rose 15%. Much of the gap is a data effect: after a carrier change, only 26% of freight used activity data.
Intensity: <b>{base.intensity_t_per_gbp_m:.1f} → {latest.intensity_t_per_gbp_m:.1f} tCO₂e per £m GMV</b>. Use this as
ADJOAA's comparison point once its first footprint is measured.</div>""", unsafe_allow_html=True)

    st.subheader("Scenario calculator — growth vs emissions")
    who = st.radio("Company", ["ADJOAA (enter your numbers)", "Wolf & Badger (FY2024 actual)"], horizontal=True)
    c1, c2, c3 = st.columns(3)
    if who.startswith("Wolf"):
        gmv0, e0 = float(latest.gmv_gbp_m), float(latest.total_reported_t)
        c1.metric("GMV FY2024", f"£{gmv0:.1f}m")
        c2.metric("Emissions FY2024", f"{e0:,.0f} t")
        c3.metric("Intensity", f"{e0 / gmv0:.1f} t/£m")
    else:
        gmv0 = c1.number_input("ADJOAA annual GMV (£m)", min_value=0.01, value=1.0, step=0.1,
                               help="Placeholder — replace with the real figure")
        use_proxy = c3.toggle("No footprint yet: use W&B intensity as proxy", value=True)
        e0 = gmv0 * float(latest.intensity_t_per_gbp_m) if use_proxy else \
            c2.number_input("ADJOAA measured emissions (tCO₂e)", min_value=0.0, value=150.0, step=10.0)
        if use_proxy:
            c2.metric("Estimated emissions (proxy)", f"{e0:,.0f} t", help="GMV × W&B 143.1 t/£m — replace once measured")
    d1, d2, d3, d4 = st.columns(4)
    growth = d1.slider("GMV growth per year", 0, 100, 30 if who.startswith("ADJOAA") else 15, 5, format="%d%%") / 100
    decarb = d2.slider("Intensity improvement per year", 0, 30, 5, 1, format="%d%%",
                       help="Carrier activity data, greener lanes, fewer returns, made-to-order, lighter packaging") / 100
    tgt = d3.slider("Target: cut in intensity by 2030", 0, 80, 42, 1, format="%d%%",
                    help="For a fast-growing SME an intensity target is often more realistic than an absolute one") / 100
    horizon = d4.slider("Horizon", 2030, 2035, 2035)
    years = list(range(2024, horizon + 1))
    gmv = [gmv0 * (1 + growth) ** (y - 2024) for y in years]
    i0 = e0 / gmv0
    bau = [g * i0 for g in gmv]
    scen = [g * i0 * (1 - decarb) ** (y - 2024) for y, g in zip(years, gmv)]
    tgt_int = [i0 - (i0 * tgt) * min(y - 2024, 6) / 6 for y in years]
    fig = go.Figure()
    fig.add_scatter(x=years, y=bau, name="Emissions — business as usual", line=dict(color=CLAY, dash="dash"))
    fig.add_scatter(x=years, y=scen, name=f"Emissions — −{decarb:.0%}/yr intensity", line=dict(color=SKY, width=3))
    fig.add_scatter(x=years, y=[g * t for g, t in zip(gmv, tgt_int)], name=f"Emissions if the intensity target (−{tgt:.0%}) is met",
                    line=dict(color=GREEN, dash="dot", width=3))
    fig.update_layout(title="Projected emissions (tCO₂e) — projections, not forecasts", xaxis=dict(dtick=1), **LAYOUT)
    st.plotly_chart(fig, width="stretch")
    k = st.columns(3)
    i2030 = i0 * (1 - decarb) ** 6
    k[0].metric("Intensity 2030 — your scenario", f"{i2030:.1f} t/£m", f"{pct(i2030, i0):+.0%}", delta_color="inverse")
    k[1].metric("Intensity 2030 — target", f"{i0 * (1 - tgt):.1f} t/£m")
    k[2].metric("Annual improvement needed", f"{1 - (1 - tgt) ** (1 / 6):.1%}")
    st.caption("Absolute emissions keep rising under most growth assumptions. W&B shows why a growing marketplace "
               "should pair an intensity target with better freight data before committing to absolute or net-zero dates.")

# ============================================================================= 6. DATA & METHODS
with tabs[5]:
    st.markdown("""
**Sources (benchmark):** Wolf & Badger Sustainability Report 2022 (summary article, Feb 2023); B Corp Impact Report 2023;
Annual Impact Reports 2024 (FY2023) and 2025 (FY2024); B Lab public directory (overall 108.8, Governance 19.0).
**ADJOAA:** public figures (brands, countries, 1% of profits commitment) from ADJOAA's website and the ICT Pulse interview
(Sep 2025). All other ADJOAA values are entered by the team in the tracker.
""")
    k = st.columns(4)
    k[0].metric("W&B KPIs assessed for data quality", len(kq))
    kq["quality_score"] = pd.to_numeric(kq.quality_score, errors="coerce")
    k[1].metric("With any public disclosure", f"{(kq.quality_score > 0).sum()} / {len(kq)}")
    k[2].metric("Average quality score", f"{kq.quality_score.mean():.1f} / 100")
    k[3].metric("Third-party assured KPIs", "0")
    st.markdown("""
- **Quality score** = accuracy + completeness + timeliness + consistency (25 points each).
- W&B's FY2023 emissions were **restated** (7,619 → 6,650 t). The dashboard uses restated values.
- W&B's FY2024 freight is 74% spend-based, so the reported +55% partly reflects the calculation method (company like-for-like ≈ +15%).
- Energy, water and waste are **not disclosed** by W&B. These are gaps ADJOAA can close early to differentiate.
- Scenario charts are what-if tools, not forecasts. B Impact area scores for 2025 are read from a report chart.
""")
    with st.expander("W&B emissions data"):
        st.dataframe(em, hide_index=True, width="stretch")
    with st.expander("W&B KPI disclosure-quality inventory"):
        st.dataframe(kq, hide_index=True, width="stretch")

st.divider()
st.caption("Independent analysis prepared from public reports for ADJOAA's internal planning. "
           "Not affiliated with or endorsed by Wolf & Badger or B Lab.")
