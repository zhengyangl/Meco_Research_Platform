"""
Data Explorer · Manufactured Ecosystems Research Database
"""

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

# ════════════════════════════════════════════════════════════════
# PAGE CONFIG 
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Explorer · MEco",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded", # 默认展开侧边栏
)

# ════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Base configuration */
.stApp { background: #F8FAFC; color: #0F172A; }
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
section.main > div { padding-top: 1rem; padding-bottom: 2rem; }
div.block-container { max-width: 1440px; padding-left: 2rem; padding-right: 2rem; }

/* Sidebar Polish */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* Typography */
.exp-eyebrow {
    font: 600 0.7rem/1 'JetBrains Mono', monospace !important;
    letter-spacing: .05em !important; text-transform: uppercase !important;
    color: #2563EB !important; margin-bottom: .4rem !important;
}
.exp-title {
    font: 600 1.8rem/1.2 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
    color: #0F172A !important; margin-bottom: .4rem !important;
}
.exp-sub {
    font: 400 0.9rem/1.5 'Inter', sans-serif !important;
    color: #64748B !important; max-width: 800px !important; margin-bottom: 1rem !important;
}

/* Navigation & Widgets */
.hero-nav { margin-bottom: 1rem; }
.hn-secondary {
    font: 500 .75rem/1 'Inter', sans-serif !important; 
    padding: 6px 12px !important; border-radius: 4px !important; 
    text-decoration: none !important; background: #FFFFFF !important; 
    color: #334155 !important; border: 1px solid #CBD5E1 !important;
    transition: all .15s; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.hn-secondary:hover {
    border-color: #94A3B8 !important; color: #0F172A !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Metric Pills */
.match-count {
    font: 500 .85rem/1 'Inter', sans-serif; color: #334155;
    padding: .5rem .8rem; background: #FFFFFF;
    border: 1px solid #E2E8F0; border-radius: 6px;
    display: inline-block; box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    margin-right: 10px;
}
.match-count b { 
    font-family: 'JetBrains Mono', monospace; 
    color: #2563EB; font-weight: 700; font-size: 0.95rem;
}

/* Charts & Buttons */
.chart-label {
    font: 600 0.75rem/1 'Inter', sans-serif !important;
    color: #475569 !important; border-bottom: 1px solid #E2E8F0;
    padding-bottom: 0.4rem; margin-bottom: 0.8rem !important;
}
div[data-testid="stDownloadButton"] button {
    background: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
    color: #0F172A !important; border-radius: 4px !important;
    font: 500 .8rem/1 'Inter', sans-serif !important;
}
div[data-testid="stDownloadButton"] button:hover {
    border-color: #2563EB !important; color: #2563EB !important;
}

/* Widget Text */
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label {
    font: 600 .7rem/1.2 'Inter', sans-serif !important;
    color: #475569 !important; text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# DATA LOADING & PRE-CACHING 
# ════════════════════════════════════════════════════════════════
_DATA_DIR = Path(__file__).parent.parent / "dashboard_data"

@st.cache_data
def load_data() -> tuple:
    # 1. Load DataFrame
    df = pd.read_parquet(_DATA_DIR / "papers_classified.parquet")
    df["pub_year"]    = pd.to_numeric(df["pub_year"], errors="coerce").astype("Int64")
    df["times_cited"] = pd.to_numeric(df["times_cited"], errors="coerce").fillna(0).astype(int)
    df["open_access"] = df["open_access"].fillna("Closed")
    
    # 2. Pre-compute dropdown options to save CPU cycles on reruns
    options = {
        "years": sorted(df["pub_year"].dropna().unique().tolist()),
        "categories": ["Replace", "Enhance", "Support"],
        "families": sorted(df["service_category"].dropna().unique().tolist()),
        "services": sorted(df["ecosystem_service"].dropna().unique().tolist()),
        "oa": sorted(df["open_access"].dropna().unique().tolist())
    }
    
    # 3. Load Meta
    with open(_DATA_DIR / "corpus_meta.json", encoding="utf-8") as f:
        meta = json.load(f)
    
    # 4. Pre-compute Impact Tier thresholds — relative to the FULL corpus.
    # These never change as the user filters, so "Top 1%" always means
    # "Top 1% of all 31,559 papers", which is an absolute impact signal.
    # The user can then see how many high-impact papers fall within their
    # current filter slice.
    _cits = df["times_cited"].values
    tiers = {
        "top_1_threshold":   int(pd.Series(_cits).quantile(0.99)),
        "top_10_threshold":  int(pd.Series(_cits).quantile(0.90)),
        "median_threshold":  int(pd.Series(_cits).quantile(0.50)),
        # Anything strictly below the median (i.e. bottom half) we treat as "tail".
        # The exact 0.50 quantile becomes the boundary between Median and Tail.
    }
        
    return df, options, meta, tiers

df_all, OPTIONS, META, TIERS = load_data()

# Compute the OA percentage once — used in the header health bar.
_OA_PCT = round((df_all["open_access"] != "Closed").mean() * 100)
_MEDIAN_CITED = int(df_all["times_cited"].median())

# ════════════════════════════════════════════════════════════════
# URL STATE SYNC 
# ════════════════════════════════════════════════════════════════
# Lets a researcher share a precise view by URL. Five core filters round-
# trip through st.query_params:
#     year_min, year_max, paradigm, family, service, min_cited
# Free-text search and OA status are deliberately NOT synced — search
# strings are session-scoped scratch input, and OA is a single click to
# toggle. We only sync the long-form filter state.
_qp = st.query_params
def _read_qp_list(key, valid_set):
    """Read a comma-separated multiselect default from URL, keeping only
    values that exist in the current dataset (defends against stale URLs)."""
    raw = _qp.get(key, "")
    if not raw:
        return []
    return [v for v in raw.split(",") if v in valid_set]

# Defaults driven by URL (fall back to empty / full range when absent).
_dflt_year_min = int(_qp.get("year_min", OPTIONS["years"][0]))
_dflt_year_max = int(_qp.get("year_max", OPTIONS["years"][-1]))
_dflt_paradigm = _read_qp_list("paradigm", set(OPTIONS["categories"]))
_dflt_family   = _read_qp_list("family",   set(OPTIONS["families"]))
_dflt_service  = _read_qp_list("service",  set(OPTIONS["services"]))
try:
    _dflt_min_cit = max(0, int(_qp.get("min_cited", 0)))
except (TypeError, ValueError):
    _dflt_min_cit = 0

# ════════════════════════════════════════════════════════════════
# SIDEBAR: CASCADING FILTERS
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="exp-eyebrow">Data Controls</div>', unsafe_allow_html=True)
    
    f_search = st.text_input("🔍 Global Search", placeholder="Title, author, keyword...")
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.expander("🌿 Ecological Focus", expanded=True):
        # Default values come from URL (see URL STATE SYNC above).
        f_category = st.multiselect("Paradigm (R/E/S)",
                                    options=OPTIONS["categories"],
                                    default=_dflt_paradigm)
        f_family = st.multiselect("Service Family",
                                  options=OPTIONS["families"],
                                  default=_dflt_family)
        
        if f_family:
            _valid_services = df_all[df_all["service_category"].isin(f_family)]["ecosystem_service"].unique().tolist()
            _valid_services = sorted(_valid_services)
        else:
            _valid_services = OPTIONS["services"]
        # Keep only services that survive the cascading filter.
        _dflt_service_filtered = [s for s in _dflt_service if s in _valid_services]
        f_service = st.multiselect("Ecosystem Service",
                                   options=_valid_services,
                                   default=_dflt_service_filtered)

    with st.expander("📅 Time & Impact", expanded=True):
        _min_y, _max_y = int(OPTIONS["years"][0]), int(OPTIONS["years"][-1])
        # Clamp URL-supplied years to the valid range.
        _y0 = max(_min_y, min(_max_y, _dflt_year_min))
        _y1 = max(_min_y, min(_max_y, _dflt_year_max))
        if _y0 > _y1:
            _y0, _y1 = _min_y, _max_y
        f_year = st.slider("Publication Year",
                           min_value=_min_y, max_value=_max_y,
                           value=(_y0, _y1))
        f_min_cit = st.number_input("Minimum Citations",
                                    min_value=0, value=_dflt_min_cit, step=10, 
                                    help="Filter out newly published or low-impact papers.")

    with st.expander("📚 Publication Details", expanded=False):
        f_oa = st.multiselect("Open Access Status", options=OPTIONS["oa"], default=[])

# ════════════════════════════════════════════════════════════════
# URL STATE SYNC 
# ════════════════════════════════════════════════════════════════
_new_qp = {}
if f_year[0] != OPTIONS["years"][0]:
    _new_qp["year_min"] = str(f_year[0])
if f_year[-1] != OPTIONS["years"][-1]:
    _new_qp["year_max"] = str(f_year[-1])
if f_category:
    _new_qp["paradigm"] = ",".join(f_category)
if f_family:
    _new_qp["family"] = ",".join(f_family)
if f_service:
    _new_qp["service"] = ",".join(f_service)
if f_min_cit > 0:
    _new_qp["min_cited"] = str(f_min_cit)

# Only write if something changed — avoids extra reruns on every interaction.
_current_qp = dict(st.query_params)
if _new_qp != _current_qp:
    st.query_params.clear()
    for k, v in _new_qp.items():
        st.query_params[k] = v

# ════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ════════════════════════════════════════════════════════════════
df = df_all
df = df[(df["pub_year"] >= f_year[0]) & (df["pub_year"] <= f_year[1])]
if f_category: df = df[df["category"].isin(f_category)]
if f_family:   df = df[df["service_category"].isin(f_family)]
if f_service:  df = df[df["ecosystem_service"].isin(f_service)]
if f_oa:       df = df[df["open_access"].isin(f_oa)]
if f_min_cit > 0: df = df[df["times_cited"] >= f_min_cit]

if f_search:
    q = f_search.lower()
    mask = (
        df["title"].fillna("").str.lower().str.contains(q, na=False) |
        df["authors"].fillna("").str.lower().str.contains(q, na=False) |
        df["keywords"].fillna("").str.lower().str.contains(q, na=False) |
        df["technology"].fillna("").str.lower().str.contains(q, na=False)
    )
    df = df[mask]

# ════════════════════════════════════════════════════════════════
# MAIN AREA: HEADER + HEALTH BAR
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-nav">
  <a class="hn-secondary" href="/">← Back to the story</a>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 class="exp-title">{len(df_all):,} Bio-inspired Papers.</h1>',
            unsafe_allow_html=True)

# Health bar — single line of immutable metadata about the corpus itself.
# Lives directly under the title so users instantly see "what version of the
# data am I looking at" without having to dig into a methodology panel.
st.markdown(
    f"""<div style="
        font: 500 .72rem/1.4 'JetBrains Mono', monospace;
        color: #64748B; margin: 0.2rem 0 1.2rem;
        padding-bottom: 0.7rem; border-bottom: 1px solid #E2E8F0;
    ">
      <b style="color:#0F172A;">{len(df_all):,}</b> papers
      &nbsp;·&nbsp; data as of {META.get("dataset_version", "—")}
      &nbsp;·&nbsp; {META.get("n_services", 22)} services
      &nbsp;·&nbsp; open access: {_OA_PCT}%
      &nbsp;·&nbsp; median citations: {_MEDIAN_CITED}
    </div>""",
    unsafe_allow_html=True
)

# Current-filter summary pill (kept from prior version but trimmed).
if len(df) > 0:
    st.markdown(
        f'<div class="match-count"><b>{len(df):,}</b> of {len(df_all):,} matched · '
        f'<b>{df["times_cited"].sum():,}</b> citations · '
        f'<b>{df["ecosystem_service"].nunique()}</b> services represented</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="match-count" style="color:#94A3B8;"><b>0</b> matched · '
        'try widening your filters</div>',
        unsafe_allow_html=True
    )

# ════════════════════════════════════════════════════════════════
# IMPACT TIERS 
# ════════════════════════════════════════════════════════════════
# Thresholds are computed once against the FULL corpus, so "Top 1%" always
# means "Top 1% of all 31,559 papers" regardless of how the user filters.
# What changes under filtering is HOW MANY of the user's current selection
# fall into each tier — an absolute impact signal, not a relative one.
st.markdown('<div style="margin-top:1.0rem;"></div>', unsafe_allow_html=True)

_t1, _t2, _t3, _t4 = st.columns(4)
def _tier_card(col, label, count, threshold_text, accent):
    col.markdown(f"""
    <div style="
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-left: 3px solid {accent};
        border-radius: 6px; padding: .85rem 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    ">
      <div style="font: 500 .65rem/1 'Inter',sans-serif;
                  color: #64748B; text-transform: uppercase;
                  letter-spacing: .08em; margin-bottom: .35rem;">
        {label}
      </div>
      <div style="font: 700 1.5rem/1 'JetBrains Mono',monospace;
                  color: #0F172A; margin-bottom: .25rem;">
        {count:,}
      </div>
      <div style="font: 400 .7rem/1.3 'Inter',sans-serif; color: #94A3B8;">
        {threshold_text}
      </div>
    </div>
    """, unsafe_allow_html=True)

if len(df) > 0:
    _n_top1   = int((df["times_cited"] >= TIERS["top_1_threshold"]).sum())
    _n_top10  = int((df["times_cited"] >= TIERS["top_10_threshold"]).sum())
    _n_median = int(((df["times_cited"] >= TIERS["median_threshold"]) &
                     (df["times_cited"] < TIERS["top_10_threshold"])).sum())
    _n_tail   = int((df["times_cited"] < TIERS["median_threshold"]).sum())
else:
    _n_top1 = _n_top10 = _n_median = _n_tail = 0

_tier_card(_t1, "Top 1%",   _n_top1,
           f"≥ {TIERS['top_1_threshold']:,} citations",   "#DC2626")
_tier_card(_t2, "Top 10%",  _n_top10,
           f"≥ {TIERS['top_10_threshold']:,} citations",  "#F59E0B")
_tier_card(_t3, "Median",   _n_median,
           f"{TIERS['median_threshold']:,}–{TIERS['top_10_threshold']:,} citations", "#2563EB")
_tier_card(_t4, "Long tail", _n_tail,
           f"< {TIERS['median_threshold']:,} citations",  "#94A3B8")

# ════════════════════════════════════════════════════════════════
# THREE CHARTS (no toggle) — Publication Trend / Top Services / Paradigm
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.6rem;"></div>', unsafe_allow_html=True)

_v1, _v2, _v3 = st.columns(3)

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#F8FAFC", plot_bgcolor="#F8FAFC",
        height=200, margin=dict(l=10, r=10, t=10, b=20),
        xaxis=dict(tickfont=dict(size=10, color="#64748B"),
                   gridcolor="#E2E8F0", linecolor="#CBD5E1"),
        yaxis=dict(tickfont=dict(size=10, color="#64748B"),
                   gridcolor="#E2E8F0", linecolor="#CBD5E1"),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#CBD5E1",
                        font=dict(size=11, color="#0F172A")),
    )
    return fig

if len(df) > 0:
    with _v1:
        st.markdown('<div class="chart-label">Publication Trend</div>',
                    unsafe_allow_html=True)
        by_year = df.groupby("pub_year").size().reset_index(name="n")
        fig_year = go.Figure(go.Scatter(
            x=by_year["pub_year"], y=by_year["n"], mode="lines",
            line=dict(color="#2563EB", width=2.5),
            fill="tozeroy", fillcolor="rgba(37,99,235,0.1)",
            hovertemplate="<b>%{x}</b><br>%{y:,} papers<extra></extra>"
        ))
        st.plotly_chart(style_fig(fig_year), use_container_width=True,
                        config={"displayModeBar": False})

    with _v2:
        st.markdown('<div class="chart-label">Top Services</div>',
                    unsafe_allow_html=True)
        by_svc = df["ecosystem_service"].value_counts().head(5).reset_index()
        by_svc.columns = ["ecosystem_service", "n"]
        fig_svc = go.Figure(go.Bar(
            y=by_svc["ecosystem_service"][::-1],
            x=by_svc["n"][::-1], orientation="h",
            marker=dict(color="#64748B"),
            hovertemplate="<b>%{y}</b><br>%{x:,} papers<extra></extra>"
        ))
        st.plotly_chart(style_fig(fig_svc), use_container_width=True,
                        config={"displayModeBar": False})

    with _v3:
        st.markdown('<div class="chart-label">Paradigm Split</div>',
                    unsafe_allow_html=True)
        by_cat = df["category"].value_counts()
        cats = ["Replace", "Enhance", "Support"]
        vals = [int(by_cat.get(c, 0)) for c in cats]
        fig_cat = go.Figure(go.Pie(
            labels=cats, values=vals, hole=0.6,
            marker=dict(colors=["#D97706", "#059669", "#2563EB"],
                        line=dict(color="#F8FAFC", width=2)),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value:,} papers<extra></extra>"
        ))
        fig_cat = style_fig(fig_cat)
        fig_cat.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                        font=dict(size=10))
        )
        st.plotly_chart(fig_cat, use_container_width=True,
                        config={"displayModeBar": False})
else:
    st.info("No data matches the selected filters.")

# ════════════════════════════════════════════════════════════════
# MAIN TABLE 
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Detailed Records</div>', unsafe_allow_html=True)

_doi_renderer = JsCode("""
class CustomDoiRenderer {
    init(params) {
        this.eGui = document.createElement('a');
        
        if (params.value) {
            const doi = params.value.replace(/^https?:\\/\\/(dx\\.)?doi\\.org\\//, '');
            this.eGui.innerText = doi + ' ↗';
            this.eGui.href = 'https://doi.org/' + doi;
            this.eGui.target = '_blank';
            this.eGui.style.color = '#2563EB';
            this.eGui.style.textDecoration = 'none';
            this.eGui.style.fontWeight = '500';
        }
    }
    
    getGui() {
        return this.eGui;
    }
}
""")

# Conditional styling for Paradigm (R/E/S)
_category_style = JsCode("""
function(params) {
    if (params.value === 'Replace') {
        return { 'color': '#92400E', 'backgroundColor': 'rgba(245, 158, 11, 0.12)', 'fontWeight': '500' };
    } else if (params.value === 'Enhance') {
        return { 'color': '#065F46', 'backgroundColor': 'rgba(16, 185, 129, 0.12)', 'fontWeight': '500' };
    } else if (params.value === 'Support') {
        return { 'color': '#1E40AF', 'backgroundColor': 'rgba(59, 130, 246, 0.12)', 'fontWeight': '500' };
    }
    return null;
}
""")

_grid_cols = [
    "title", "authors", "pub_year", "source_title", "times_cited",
    "open_access", "ecosystem_service", "service_category", "category",
    "technology", "doi",
]
if len(df) == 0:
    st.info("No papers match the current filters. Try clearing some constraints in the sidebar.")
    st.stop()   # don't render the empty AgGrid below

df_grid = df[_grid_cols].copy()

gb = GridOptionsBuilder.from_dataframe(df_grid)
gb.configure_default_column(filter=True, sortable=True, resizable=True, wrapText=True, autoHeight=False)

gb.configure_column("title", header_name="Title", minWidth=250, width=280, wrapText=True, autoHeight=True, pinned="left")

gb.configure_column("authors",            header_name="Authors",            minWidth=180, flex=2)
gb.configure_column("pub_year",           header_name="Year",               width=80, type=["numericColumn"])
gb.configure_column("source_title",       header_name="Journal",            minWidth=160, flex=1.5)
gb.configure_column("times_cited",        header_name="Citations",          width=100, type=["numericColumn"], sort="desc")
gb.configure_column("open_access",        header_name="Access",             width=110)
gb.configure_column("ecosystem_service",  header_name="Ecosystem Service",  minWidth=160, flex=1.5)
gb.configure_column("service_category",   header_name="Family",             width=120)

# CONDITIONAL STYLING applied here
gb.configure_column("category",           header_name="Paradigm",           width=110, cellStyle=_category_style)

gb.configure_column("technology",         header_name="Technology",         minWidth=160, flex=1.5)
gb.configure_column("doi",                header_name="DOI",                minWidth=200, flex=1.5, cellRenderer=_doi_renderer)

gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
gb.configure_grid_options(domLayout="normal", suppressMenuHide=True, rowHeight=40)

AgGrid(
    df_grid,
    gridOptions=gb.build(),
    height=600,
    theme="balham", # Professional compact theme
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.NO_UPDATE,
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=False,
)

# ════════════════════════════════════════════════════════════════
# METHODOLOGY PANEL 
# ════════════════════════════════════════════════════════════════
# Folded by default so it doesn't compete with the main UI, but always
# one click away. The point is to make every step from raw WoS export to
# the numbers on this page auditable without leaving the page.
st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)
with st.expander("📊 How were these papers classified? (Methodology & data lineage)"):
    st.markdown(f"""
**Source corpus.** {META.get("total_papers", 68917):,} unique publications
retrieved from Web of Science using `biomim*` / `bioinspir*` queries,
2004–2025. After removing {META.get("reviews", 9318):,} review articles,
{META.get("non_review", 59599):,} original-research papers remained.

**Classification.** Each paper was classified by **GPT-4.1** using a
structured prompt developed for Jacobs et al. (2025). The model decides:

- **Decision (Y/N):** Does this paper describe a technology contributing
  to at least one ecosystem service? Yes for **{META.get("decision_y", 31559):,}**
  papers (≈ {round(META.get("decision_y", 31559) / META.get("non_review", 59599) * 100)}% of non-reviews).
- **Category (R/E/S):** Does the technology *Replace*, *Enhance*, or *Support*
  the natural process? Boundaries defined in the published prompt.
- **Ecosystem service:** Which of the 22 services (per Costanza et al. 1997
  + IPBES extensions) does it target?
- **Technology:** Free-text label for the bio-inspired technology described.

**Defensive filtering.** Two LLM hallucination values (`"Cultural"`,
`"Ecosystem monitoring"`) appeared in initial outputs and were filtered
out by a 22-service whitelist in `aggregate.py`. Both edge cases happened
to be review articles, so they would have been excluded by the
`is_review = FALSE` filter regardless.

**Versioning.** Every classification result is stored in PostgreSQL with
its `model_version`, `prompt_version`, and `run_id`. When the corpus is
re-classified with a newer model, historical results are preserved —
the dashboard always reads `is_current = TRUE` rows. Raw LLM JSON
responses are kept in the `classification_audit` table for replication.

**Reproduce these numbers.** The full pipeline (ingestion → LLM classify
→ aggregate → static JSON/Parquet) lives in `pipeline/`. See
`docs/handover.md` for the 5-step update procedure.

*Data version: {META.get("dataset_version", "—")} ·
Aggregate generated: {META.get("generated_at", "—")}*
    """)
# ════════════════════════════════════════════════════════════════
# EXPORT & SHARE
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.0rem;"></div>', unsafe_allow_html=True)

_export_col, _share_col = st.columns([1, 1])

with _export_col:
    st.markdown('<div style="font: 600 .65rem/1.2 Inter, sans-serif; letter-spacing: .05em; color: #8A847B; margin-bottom: 0.5rem; text-transform: uppercase;">Export Data</div>', unsafe_allow_html=True)
    _csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇ Download Current {len(df):,} Records as CSV",
        data=_csv,
        file_name=f"meco_filtered_export.csv",
        mime="text/csv",
    )

with _share_col:
    st.markdown('<div style="font: 600 .65rem/1.2 Inter, sans-serif; letter-spacing: .05em; color: #8A847B; margin-bottom: 0.5rem; text-transform: uppercase;">Share This View</div>', unsafe_allow_html=True)
    import urllib.parse
    current_params = st.query_params.to_dict()
    query_string = urllib.parse.urlencode(current_params, doseq=True)
    
    base_url = "https://demo-v3.streamlit.app/explorer" 
    full_share_url = f"{base_url}?{query_string}" if query_string else base_url
    
    st.text_input("share_url", value=full_share_url, label_visibility="collapsed")

st.markdown(f"""
<p style="font:400 .75rem/1.7 'Inter',sans-serif;color:#94A3B8;margin-top:1.4rem;">
    Data as of {META.get("dataset_version", "—")} · Derived from 31,559 Decision='Y' non-review papers · 
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#64748B;text-decoration:underline;">
    View base methodology →</a>
</p>
""", unsafe_allow_html=True)
