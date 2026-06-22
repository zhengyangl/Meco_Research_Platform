"""
Data Explorer · Manufactured Ecosystems Research Database
==========================================================
Companion page to the narrative dashboard. Where the narrative curates a
story from the data, this page lets researchers slice the corpus themselves:
filter by year / category / open access / journal, see the distribution
shift live, and export the matching rows.

Data source: dashboard_data/papers_classified.parquet (produced by
pipeline/aggregate.py — 31,559 Decision='Y' non-review papers, 17 columns).

Dependencies (additions to requirements.txt):
    streamlit-aggrid>=1.0.5
"""

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode


# ════════════════════════════════════════════════════════════════
# PAGE CONFIG  (sidebar hidden by CSS below)
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Explorer · MEco",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ════════════════════════════════════════════════════════════════
# GLOBAL CSS — matches the narrative page's typography, with extras
# for the sticky filter bar and the explorer-specific palette
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base — match the narrative page so users feel they're in the same product ── */
.stApp { background: #F7F5F1; color: #2A2722; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
section.main > div { padding-top: 1.2rem; padding-bottom: 4rem; }
div.block-container { max-width: 1280px; padding-left: 2rem; padding-right: 2rem; }

/* ── Header ─────────────────────────────────────────────────── */
.exp-eyebrow {
    font: 500 0.68rem/1 'Inter', sans-serif !important;
    letter-spacing: .22em !important; text-transform: uppercase !important;
    color: #3D7A52 !important; margin-bottom: .85rem !important;
}
.exp-title {
    font: 700 2.6rem/1.08 'Playfair Display', serif !important;
    color: #2A2722 !important; margin-bottom: .5rem !important;
}
.exp-sub {
    font: 300 1.0rem/1.7 'Inter', sans-serif !important;
    color: #6B665E !important; max-width: 720px !important; margin-bottom: 1.4rem !important;
}

/* ── Hero nav (mirrors the narrative page's pills) ── */
.hero-nav { display: flex; gap: 10px; align-items: flex-start; flex-wrap: wrap;
            margin-bottom: 1.4rem; }
.hn-secondary {
    font: 500 .74rem/1 'Inter', sans-serif !important; letter-spacing: .02em !important;
    padding: 9px 16px !important; border-radius: 20px !important; text-decoration: none !important;
    background: #FFFFFF !important; color: #4A453E !important;
    border: 1px solid #E5E1DA !important;
    transition: background .18s, border-color .18s, color .18s;
}
.hn-secondary:hover {
    border-color: rgba(61,122,82,0.45) !important;
    background: rgba(61,122,82,0.05) !important; color: #2A2722 !important;
}

/* ── Sticky filter bar ── */
.filter-bar-wrap {
    position: sticky; top: 0; z-index: 50;
    background: rgba(247, 245, 241, 0.96);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    border-bottom: 1px solid #E5E1DA;
    padding: 1rem 0 .8rem;
    margin: 0 -2rem 1.4rem;
    padding-left: 2rem; padding-right: 2rem;
}
.filter-label {
    font: 500 .66rem/1 'Inter', sans-serif !important;
    letter-spacing: .14em !important; text-transform: uppercase !important;
    color: #8A847B !important; margin-bottom: .35rem !important;
}
.match-count {
    font: 400 .88rem/1 'Inter', sans-serif; color: #4A453E;
    padding: .55rem 1rem; background: rgba(61,122,82,0.07);
    border: 1px solid rgba(61,122,82,0.20); border-radius: 20px;
    display: inline-block;
}
.match-count b { color: #356B49; font-weight: 600; }

/* ── Chart caption ── */
.chart-label {
    font: 500 0.68rem/1 'Inter', sans-serif !important;
    letter-spacing: .18em !important; text-transform: uppercase !important;
    color: #8A847B !important; margin-bottom: .6rem !important;
}

/* ── Streamlit widget polish ── */
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font: 500 .66rem/1.3 'Inter', sans-serif !important;
    letter-spacing: .14em !important; text-transform: uppercase !important;
    color: #8A847B !important;
}

/* ── Download button (reuses narrative page's styling) ── */
div[data-testid="stDownloadButton"] button {
    background: rgba(61,122,82,0.08) !important;
    border: 1px solid rgba(61,122,82,0.40) !important;
    color: #356B49 !important;
    font: 500 .76rem/1 'Inter', sans-serif !important;
    letter-spacing: .04em !important;
    height: auto !important; padding: .6rem 1.4rem !important;
    box-shadow: none !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(61,122,82,0.14) !important;
    border-color: rgba(61,122,82,0.65) !important;
    color: #2A2722 !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# DATA LOADING — read the parquet produced by aggregate.py
# ════════════════════════════════════════════════════════════════
_DATA_DIR = Path(__file__).parent.parent / "dashboard_data"

@st.cache_data
def load_papers() -> pd.DataFrame:
    df = pd.read_parquet(_DATA_DIR / "papers_classified.parquet")
    # Defensive: parquet should already have these dtypes, but enforce here
    # so downstream filters don't get tripped up by stray NaN-as-float values.
    df["pub_year"]    = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df["times_cited"] = pd.to_numeric(df["times_cited"], errors="coerce").fillna(0).astype(int)
    df["open_access"] = df["open_access"].fillna("Closed")
    return df

@st.cache_data
def load_meta() -> dict:
    with open(_DATA_DIR / "corpus_meta.json", encoding="utf-8") as f:
        return json.load(f)

df_all = load_papers()
META = load_meta()


# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-nav">
  <a class="hn-secondary" href="/">← Back to the story</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="exp-eyebrow">Data Explorer · Manufactured Ecosystems</div>',
            unsafe_allow_html=True)
st.markdown(f'<h1 class="exp-title">{len(df_all):,} Bio-inspired Research Papers.</h1>',
            unsafe_allow_html=True)
st.markdown(f"""
<p class="exp-sub">
    Every paper in this table has been classified as bio-inspired research
    targeting at least one of the 22 ecosystem services. Filter, sort, and
    export below. Source: Jacobs et al. (2025) · data as of {META.get("dataset_version", "—")}.
</p>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# STICKY FILTER BAR
# ════════════════════════════════════════════════════════════════
# Wrapped in a div with class 'filter-bar-wrap' so the CSS above can pin
# it to the top of the viewport. The opening <div> goes here; the closing
# </div> goes immediately after the last filter widget.
st.markdown('<div class="filter-bar-wrap">', unsafe_allow_html=True)

# Pre-compute filter option lists from the full dataset, sorted nicely.
_years = sorted(df_all["pub_year"].dropna().unique().tolist())
_min_year, _max_year = int(_years[0]), int(_years[-1])
_all_categories = ["Replace", "Enhance", "Support"]
_all_services   = sorted(df_all["ecosystem_service"].dropna().unique().tolist())
_all_families   = sorted(df_all["service_category"].dropna().unique().tolist())
_all_oa         = sorted(df_all["open_access"].dropna().unique().tolist())

# Row 1: year range, paradigm, service family, ecosystem service
_c1, _c2, _c3, _c4 = st.columns([1.2, 1, 1, 1.3])
with _c1:
    f_year = st.slider("Year range",
                       min_value=_min_year, max_value=_max_year,
                       value=(_min_year, _max_year), step=1)
with _c2:
    f_category = st.multiselect("Paradigm (R/E/S)",
                                options=_all_categories, default=[])
with _c3:
    f_family = st.multiselect("Service family",
                              options=_all_families, default=[])
with _c4:
    f_service = st.multiselect("Ecosystem service",
                               options=_all_services, default=[])

# Row 2: open access, min citations, search
_c5, _c6, _c7 = st.columns([1, 1.2, 2])
with _c5:
    f_oa = st.multiselect("Open access status",
                          options=_all_oa, default=[])
with _c6:
    f_min_cit = st.number_input("Min. citations", min_value=0, value=0, step=10)
with _c7:
    f_search = st.text_input("Search title / authors / keywords / technology",
                             placeholder="e.g. RoboBee, photosynthesis, nanofiber...")

# Close the sticky wrapper. The "X papers match" pill below it lives outside
# the sticky band so it scrolls with the page (and feels more like a
# "results summary" than a filter widget).
st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ════════════════════════════════════════════════════════════════
# Build the filtered frame in one pass. Each step starts from the previous
# result; empty multiselects are treated as "no constraint", which is the
# conventional behaviour for facet-style filters.
df = df_all
df = df[(df["pub_year"] >= f_year[0]) & (df["pub_year"] <= f_year[1])]
if f_category:
    df = df[df["category"].isin(f_category)]
if f_family:
    df = df[df["service_category"].isin(f_family)]
if f_service:
    df = df[df["ecosystem_service"].isin(f_service)]
if f_oa:
    df = df[df["open_access"].isin(f_oa)]
if f_min_cit > 0:
    df = df[df["times_cited"] >= f_min_cit]
if f_search:
    # Case-insensitive substring search across the four most-relevant text
    # columns. NaN-safe (str.contains with na=False).
    q = f_search.lower()
    mask = (
        df["title"].fillna("").str.lower().str.contains(q, na=False) |
        df["authors"].fillna("").str.lower().str.contains(q, na=False) |
        df["keywords"].fillna("").str.lower().str.contains(q, na=False) |
        df["technology"].fillna("").str.lower().str.contains(q, na=False)
    )
    df = df[mask]

# Results summary pill — sits just under the sticky filter band.
st.markdown(
    f'<div class="match-count"><b>{len(df):,}</b> papers match · '
    f'<b>{df["times_cited"].sum():,}</b> total citations · '
    f'<b>{df["ecosystem_service"].nunique()}</b> services represented</div>',
    unsafe_allow_html=True
)


# ════════════════════════════════════════════════════════════════
# LINKED VISUALIZATIONS (3 small charts that update with filters)
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.6rem;"></div>', unsafe_allow_html=True)
_v1, _v2, _v3 = st.columns(3)

# ── Chart 1: papers per year ─────────────────────────────────────
with _v1:
    st.markdown('<div class="chart-label">Papers per year</div>', unsafe_allow_html=True)
    if len(df) == 0:
        st.markdown("<div style='color:#B8B0A4;font:300 .82rem/1.6 Inter,sans-serif;'>No data to display.</div>",
                    unsafe_allow_html=True)
    else:
        by_year = df.groupby("pub_year").size().reset_index(name="n")
        fig_year = go.Figure()
        fig_year.add_trace(go.Scatter(
            x=by_year["pub_year"], y=by_year["n"], mode="lines+markers",
            line=dict(color="#3D7A52", width=2),
            marker=dict(color="#3D7A52", size=5),
            fill="tozeroy", fillcolor="rgba(61,122,82,0.12)",
            hovertemplate="<b>%{x}</b><br>%{y:,} papers<extra></extra>",
        ))
        fig_year.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FBF9F5",
            height=240, margin=dict(l=40, r=10, t=10, b=30),
            xaxis=dict(tickfont=dict(size=10, color="#8A847B"),
                       gridcolor="#ECE8E1", linecolor="#E5E1DA"),
            yaxis=dict(tickfont=dict(size=10, color="#8A847B"),
                       gridcolor="#ECE8E1", linecolor="#E5E1DA", tickformat=","),
            hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                            font=dict(size=11, color="#2A2722")),
        )
        st.plotly_chart(fig_year, use_container_width=True, config={"displayModeBar": False})

# ── Chart 2: top 10 ecosystem services ───────────────────────────
with _v2:
    st.markdown('<div class="chart-label">Top services (by paper count)</div>', unsafe_allow_html=True)
    if len(df) == 0:
        st.markdown("<div style='color:#B8B0A4;font:300 .82rem/1.6 Inter,sans-serif;'>No data to display.</div>",
                    unsafe_allow_html=True)
    else:
        by_svc = df["ecosystem_service"].value_counts().head(10).reset_index()
        by_svc.columns = ["service", "n"]
        # Reverse for horizontal bar (largest at top)
        by_svc = by_svc.iloc[::-1]
        fig_svc = go.Figure()
        fig_svc.add_trace(go.Bar(
            y=by_svc["service"], x=by_svc["n"], orientation="h",
            marker=dict(color="#2E7CB8", line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>%{x:,} papers<extra></extra>",
        ))
        fig_svc.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FBF9F5",
            height=240, margin=dict(l=10, r=10, t=10, b=30),
            xaxis=dict(tickfont=dict(size=10, color="#8A847B"),
                       gridcolor="#ECE8E1", linecolor="#E5E1DA", tickformat=","),
            yaxis=dict(tickfont=dict(size=9, color="#4A453E"),
                       linecolor="#E5E1DA"),
            hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                            font=dict(size=11, color="#2A2722")),
        )
        st.plotly_chart(fig_svc, use_container_width=True, config={"displayModeBar": False})

# ── Chart 3: R/E/S paradigm split ────────────────────────────────
with _v3:
    st.markdown('<div class="chart-label">Paradigm split (R/E/S)</div>', unsafe_allow_html=True)
    if len(df) == 0:
        st.markdown("<div style='color:#B8B0A4;font:300 .82rem/1.6 Inter,sans-serif;'>No data to display.</div>",
                    unsafe_allow_html=True)
    else:
        by_cat = df["category"].value_counts()
        # Force the canonical R/E/S order even when one bucket is empty
        cats = ["Replace", "Enhance", "Support"]
        vals = [int(by_cat.get(c, 0)) for c in cats]
        colors = ["#A8740E", "#1D8C69", "#2E7CB8"]
        fig_cat = go.Figure(go.Pie(
            labels=cats, values=vals, hole=0.55,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=1.5)),
            textinfo="label+percent",
            textfont=dict(size=11, color="#FFFFFF", family="Inter, sans-serif"),
            hovertemplate="<b>%{label}</b><br>%{value:,} papers (%{percent})<extra></extra>",
            sort=False,
        ))
        fig_cat.update_layout(
            paper_bgcolor="#FFFFFF",
            height=240, margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                            font=dict(size=11, color="#2A2722")),
        )
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})


# ════════════════════════════════════════════════════════════════
# MAIN TABLE (AgGrid)
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Filtered papers — sortable, paginated, exportable</div>',
            unsafe_allow_html=True)

# DOI column renderer: turns plain DOI strings into clickable links that open
# the publisher's page in a new tab. JsCode injects a tiny JS function into
# AgGrid's rendering pipeline; it's the cleanest way to get hyperlinks inside
# a Streamlit grid right now.
_doi_renderer = JsCode("""
function(params) {
    if (!params.value) return '';
    const doi = params.value.replace(/^https?:\\/\\/(dx\\.)?doi\\.org\\//, '');
    return '<a href="https://doi.org/' + doi + '" target="_blank" '
         + 'style="color:#2E7CB8;text-decoration:none;">' + doi + ' ↗</a>';
}
""")

# Columns shown in the grid (a curated subset of the parquet's 17 columns —
# the rest are still in the download CSV for power users who export).
_grid_cols = [
    "title", "authors", "pub_year", "source_title", "times_cited",
    "open_access", "ecosystem_service", "service_category", "category",
    "technology", "doi",
]
df_grid = df[_grid_cols].copy()

# Build grid options — column widths and types are configured here so the
# defaults are sensible for our data (long titles wide, year narrow, etc.).
gb = GridOptionsBuilder.from_dataframe(df_grid)
gb.configure_default_column(
    filter=True, sortable=True, resizable=True,
    wrapText=True, autoHeight=False,
)
gb.configure_column("title",              header_name="Title",              minWidth=320, flex=3)
gb.configure_column("authors",            header_name="Authors",            minWidth=180, flex=2)
gb.configure_column("pub_year",           header_name="Year",               width=85, type=["numericColumn"])
gb.configure_column("source_title",       header_name="Journal",            minWidth=160, flex=1.5)
gb.configure_column("times_cited",        header_name="Citations",          width=110, type=["numericColumn"], sort="desc")
gb.configure_column("open_access",        header_name="Access",             width=110)
gb.configure_column("ecosystem_service",  header_name="Ecosystem service",  minWidth=150, flex=1)
gb.configure_column("service_category",   header_name="Family",             width=120)
gb.configure_column("category",           header_name="Paradigm",           width=110)
gb.configure_column("technology",         header_name="Technology",         minWidth=160, flex=1.5)
gb.configure_column("doi",                header_name="DOI",                minWidth=200, flex=1.5,
                                            cellRenderer=_doi_renderer)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)
gb.configure_grid_options(
    domLayout="normal",
    suppressMenuHide=True,
)

AgGrid(
    df_grid,
    gridOptions=gb.build(),
    height=620,
    theme="streamlit",
    allow_unsafe_jscode=True,           # required because we use JsCode above
    update_mode=GridUpdateMode.NO_UPDATE,
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=False,
)


# ════════════════════════════════════════════════════════════════
# EXPORT
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.0rem;"></div>', unsafe_allow_html=True)

# The download includes ALL 17 columns (more than the grid shows) — researchers
# exporting data usually want every field available, not just what's on screen.
_csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"⬇  Download these {len(df):,} papers as CSV",
    data=_csv,
    file_name=f"meco_papers_filtered_{len(df)}rows.csv",
    mime="text/csv",
)

st.markdown(f"""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#B8B0A4;margin-top:1.4rem;padding-left:2px;">
    Source: Jacobs et al. (2025), <em>Biomimetics</em> 10, 784 ·
    Classification by GPT-4.1 (full prompt and audit log in the database).
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#9A938A;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)