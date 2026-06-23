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
        
    return df, options, meta

df_all, OPTIONS, META = load_data()

# ════════════════════════════════════════════════════════════════
# SIDEBAR: CASCADING FILTERS
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="exp-eyebrow">Data Controls</div>', unsafe_allow_html=True)
    
    f_search = st.text_input("🔍 Global Search", placeholder="Title, author, keyword...")
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.expander("🌿 Ecological Focus", expanded=True):
        f_category = st.multiselect("Paradigm (R/E/S)", options=OPTIONS["categories"], default=[])
        f_family = st.multiselect("Service Family", options=OPTIONS["families"], default=[])
        
        if f_family:
            _valid_services = df_all[df_all["service_category"].isin(f_family)]["ecosystem_service"].unique().tolist()
            _valid_services = sorted(_valid_services)
        else:
            _valid_services = OPTIONS["services"]
            
        f_service = st.multiselect("Ecosystem Service", options=_valid_services, default=[])

    with st.expander("📅 Time & Impact", expanded=True):
        _min_y, _max_y = int(OPTIONS["years"][0]), int(OPTIONS["years"][-1])
        f_year = st.slider("Publication Year", min_value=_min_y, max_value=_max_y, value=(_min_y, _max_y))
        f_min_cit = st.number_input("Minimum Citations", min_value=0, value=0, step=10, 
                                    help="Filter out newly published or low-impact papers.")

    with st.expander("📚 Publication Details", expanded=False):
        f_oa = st.multiselect("Open Access Status", options=OPTIONS["oa"], default=[])

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
# MAIN AREA: HEADER & KPI PILLS
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-nav">
  <a class="hn-secondary" href="/">← Back to the story</a>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 class="exp-title">{len(df_all):,} Bio-inspired Papers.</h1>', unsafe_allow_html=True)
if len(df) > 0:
    st.markdown(
        f'<div class="match-count"><b>{len(df):,}</b> matched</div>'
        f'<div class="match-count"><b>{df["times_cited"].sum():,}</b> citations</div>'
        f'<div class="match-count"><b>{df["ecosystem_service"].nunique()}</b> services</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="match-count" style="color:#94A3B8;"><b>0</b> matched · try widening your filters</div>',
        unsafe_allow_html=True
    )

st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
view_mode = st.radio("Chart View",
                     ["Ecological Focus", "Academic Sources"],
                     horizontal=True, label_visibility="collapsed")
st.markdown('<div style="margin-top:0.6rem;"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# DYNAMIC VISUALIZATIONS
# ════════════════════════════════════════════════════════════════
_v1, _v2, _v3 = st.columns(3)

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#F8FAFC", plot_bgcolor="#F8FAFC",
        height=180, margin=dict(l=10, r=10, t=10, b=20),
        xaxis=dict(tickfont=dict(size=10, color="#64748B"), gridcolor="#E2E8F0", linecolor="#CBD5E1"),
        yaxis=dict(tickfont=dict(size=10, color="#64748B"), gridcolor="#E2E8F0", linecolor="#CBD5E1"),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#CBD5E1", font=dict(size=11, color="#0F172A")),
    )
    return fig

if len(df) > 0:
    if view_mode == "Ecological Focus":
        with _v1:
            st.markdown('<div class="chart-label">Publication Trend</div>', unsafe_allow_html=True)
            by_year = df.groupby("pub_year").size().reset_index(name="n")
            fig_year = go.Figure(go.Scatter(
                x=by_year["pub_year"], y=by_year["n"], mode="lines",
                line=dict(color="#2563EB", width=2.5), fill="tozeroy", fillcolor="rgba(37,99,235,0.1)",
                hovertemplate="<b>%{x}</b><br>%{y:,} papers<extra></extra>"
            ))
            st.plotly_chart(style_fig(fig_year), use_container_width=True, config={"displayModeBar": False})
            
        with _v2:
            st.markdown('<div class="chart-label">Top Services</div>', unsafe_allow_html=True)
            by_svc = df["ecosystem_service"].value_counts().head(5).reset_index()
            fig_svc = go.Figure(go.Bar(
                y=by_svc["ecosystem_service"][::-1], x=by_svc["count"][::-1], orientation="h",
                marker=dict(color="#64748B"), hovertemplate="<b>%{y}</b><br>%{x:,} papers<extra></extra>"
            ))
            st.plotly_chart(style_fig(fig_svc), use_container_width=True, config={"displayModeBar": False})

        with _v3:
            st.markdown('<div class="chart-label">Paradigm Split</div>', unsafe_allow_html=True)
            by_cat = df["category"].value_counts()
            cats = ["Replace", "Enhance", "Support"]
            vals = [int(by_cat.get(c, 0)) for c in cats]
            fig_cat = go.Figure(go.Pie(
                labels=cats, values=vals, hole=0.6,
                marker=dict(colors=["#D97706", "#059669", "#2563EB"], line=dict(color="#F8FAFC", width=2)),
                textinfo="none", hovertemplate="<b>%{label}</b><br>%{value:,} papers<extra></extra>"
            ))
            fig_cat = style_fig(fig_cat)
            fig_cat.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=10)))
            st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

    else: # Academic Sources View
        with _v1:
            st.markdown('<div class="chart-label">Top Journals</div>', unsafe_allow_html=True)
            by_journal = df["source_title"].value_counts().head(5)
            # Truncate only when needed; keep full name in hover tooltip.
            _labels = [(n if len(n) <= 28 else n[:27] + "…") for n in by_journal.index]
            fig_j = go.Figure(go.Bar(
                y=_labels[::-1], x=by_journal.values[::-1], orientation="h",
                customdata=list(by_journal.index)[::-1],
                marker=dict(color="#0F172A"),
                hovertemplate="<b>%{customdata}</b><br>%{x:,} papers<extra></extra>"
            ))
            st.plotly_chart(style_fig(fig_j), use_container_width=True, config={"displayModeBar": False})
            
        with _v2:
            st.markdown('<div class="chart-label">Citation Distribution (Log)</div>', unsafe_allow_html=True)
            # Most citation distributions are heavily right-skewed (long tail).
            # Plot log(1+citations) on X so the tail compresses visually
            # but the Y axis stays an intuitive "paper count".
            import numpy as _np
            _log_cit = _np.log1p(df["times_cited"])
            fig_cit = go.Figure(go.Histogram(
                x=_log_cit, nbinsx=30, marker_color="#475569",
                hovertemplate="log(1+citations) = %{x:.1f}<br>%{y} papers<extra></extra>"
            ))
            fig_cit = style_fig(fig_cit)
            fig_cit.update_xaxes(title=dict(text="log(1+citations)", font=dict(size=9, color="#94A3B8")))
            st.plotly_chart(fig_cit, use_container_width=True, config={"displayModeBar": False})

        with _v3:
            st.markdown('<div class="chart-label">Open Access Split</div>', unsafe_allow_html=True)
            by_oa = df["open_access"].value_counts()
            fig_oa = go.Figure(go.Pie(
                labels=by_oa.index, values=by_oa.values, hole=0.6,
                marker=dict(colors=["#10B981", "#94A3B8"], line=dict(color="#F8FAFC", width=2)),
                textinfo="none", hovertemplate="<b>%{label}</b><br>%{value:,} papers<extra></extra>"
            ))
            fig_oa = style_fig(fig_oa)
            fig_oa.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=10)))
            st.plotly_chart(fig_oa, use_container_width=True, config={"displayModeBar": False})
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

gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)
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
# EXPORT
# ════════════════════════════════════════════════════════════════
st.markdown('<div style="margin-top:1.0rem;"></div>', unsafe_allow_html=True)

_csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"⬇ Download Current {len(df):,} Records as CSV",
    data=_csv,
    file_name=f"meco_filtered_export.csv",
    mime="text/csv",
)

st.markdown(f"""
<p style="font:400 .75rem/1.7 'Inter',sans-serif;color:#94A3B8;margin-top:1.4rem;">
    Data as of {META.get("dataset_version", "—")} · Derived from 31,559 Decision='Y' non-review papers[cite: 1] · 
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#64748B;text-decoration:underline;">
    View base methodology →</a>
</p>
""", unsafe_allow_html=True)
