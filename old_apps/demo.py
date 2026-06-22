"""
MEco Research Dashboard — Complete Single-Page Application
"Nature Is Not Optional."
Based on Jacobs et al. (2025), Biomimetics 2025, 10, 784

Assembly instructions (run in terminal):
    cat app_part1.py app_part2.py app_part3.py app_part4.py > app.py
    streamlit run app.py
"""

# ════════════════════════════════════════════════════════════════
# IMPORTS  (all libraries used across the entire app)
# ════════════════════════════════════════════════════════════════
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# ════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must appear exactly once per Streamlit app)
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Nature Is Not Optional · MEco",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════
# GLOBAL CSS  (merged from all six sections; duplicates removed)
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ─────────────────────────────────────────────────── */
.stApp { background: #0A0E14; color: #E2DDD6; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }
section.main > div { padding-top: 2.5rem; padding-bottom: 6rem; }
div.block-container { max-width: 1080px; padding-left: 2rem; padding-right: 2rem; }

/* ── Shared utilities ─────────────────────────────────────── */
.hr     { border: none; border-top: 1px solid #161B26; margin: 1.5rem 0; }
.hr-sm  { border: none; border-top: 1px solid #161B26; margin: 1.2rem 0; }
.section-sep { border: none; border-top: 1px solid #1C2230; margin: 5rem 0 4rem; }
.chart-label {
    font: 500 0.68rem/1 'Inter', sans-serif;
    letter-spacing: .18em; text-transform: uppercase;
    color: #2E3648; margin-bottom: .6rem;
}
.chart-sub-label {
    font: 300 .82rem/1.6 'Inter', sans-serif;
    color: #3A404F; max-width: 600px; margin-bottom: .9rem;
}

/* ── All section eyebrows (identical style, kept as named classes) ── */
.hero-eyebrow, .s1-eyebrow, .s2-eyebrow,
.s3-eyebrow, .s4-eyebrow, .eyebrow {
    font: 500 0.68rem/1 'Inter', sans-serif;
    letter-spacing: .22em; text-transform: uppercase;
    color: #4A7C59; margin-bottom: .85rem;
}

/* ── Section 0: Hero ──────────────────────────────────────── */
.hero-eyebrow { font-size: 0.7rem; margin-bottom: .9rem; }
.hero-title {
    font: 700 3.8rem/1.05 'Playfair Display', serif;
    color: #E2DDD6; margin-bottom: .9rem;
}
.hero-sub {
    font: 300 1.08rem/1.8 'Inter', sans-serif;
    color: #72706A; max-width: 540px; margin-bottom: 1.8rem;
}
.hero-prompt {
    font: 400 1rem/1.7 'Inter', sans-serif;
    color: #C0BCB6; padding: 1.1rem 1.5rem;
    border-left: 3px solid #3D6B4F;
    border-radius: 0 8px 8px 0;
    background: rgba(74,124,89,.06);
}
.hero-prompt strong { color: #E2DDD6; font-weight: 500; }

/* ── Section 0: Category pills ───────────────────────────── */
.cat-pill {
    display: inline-block;
    font: 500 0.67rem/1 'Inter', sans-serif;
    letter-spacing: .16em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px;
    margin: 1.6rem 0 .8rem;
}
.cp-provisioning { background: rgba(186,117,23,.10); color: #C9901A; }
.cp-cultural      { background: rgba(127,119,221,.10); color: #8A82DD; }
.cp-regulating    { background: rgba(29,158,117,.10);  color: #1D9E75; }
.cp-supporting    { background: rgba(74,124,89,.10);   color: #5A9C6E; }

/* ── Section 0: Service cards ────────────────────────────── */
.svc-card {
    background: #10151E; border: 1px solid #1C2230;
    border-radius: 9px; padding: 12px 14px 8px;
    margin-bottom: 2px; min-height: 88px;
    transition: border-color .25s, background .25s;
}
.svc-sel-provisioning { background: rgba(186,117,23,.06); border-color: #B8943E !important; }
.svc-sel-cultural      { background: rgba(127,119,221,.06); border-color: #7A72C8 !important; }
.svc-sel-regulating    { background: rgba(29,158,117,.06);  border-color: #1D9E75 !important; }
.svc-sel-supporting    { background: rgba(74,124,89,.06);   border-color: #3D6B4F !important; }
.svc-icon { font-size: 1.3rem; display: block; margin-bottom: 5px; }
.svc-name { font: 500 .84rem/1.2 'Inter', sans-serif; color: #D8D4CD; margin-bottom: 3px; }
.svc-desc { font: 400 .7rem/1.4 'Inter', sans-serif; color: #3E4760; }

/* ── Section 0: Checkbox ─────────────────────────────────── */
div[data-testid="stCheckbox"] { margin-top: -2px !important; margin-bottom: 8px !important; }
div[data-testid="stCheckbox"] label,
div[data-testid="stCheckbox"] label p {
    font: 400 .68rem/1 'Inter', sans-serif !important;
    color: #2E3648 !important; cursor: pointer;
}
div[data-testid="stCheckbox"] label:hover,
div[data-testid="stCheckbox"] label:hover p { color: #7A8090 !important; }

/* ── Section 0: Counter ──────────────────────────────────── */
.ctr {
    text-align: center; background: #0E1320;
    border: 1px solid #1C2230; border-radius: 10px;
    padding: 1.6rem 2rem; margin: 1rem 0;
}
.ctr-n   { font: 700 3.2rem/1 'Playfair Display', serif; color: #5A9C6E; }
.ctr-sub { font: 300 .82rem/1 'Inter', sans-serif; color: #2E3648; margin-top: 6px; }

/* ── Section 0: Insight panel ────────────────────────────── */
.insight {
    background: linear-gradient(145deg, #0C1810 0%, #0A0E14 70%);
    border: 1px solid #264035; border-radius: 12px;
    padding: 2rem 2.4rem; margin-top: 1rem;
}
.insight-title { font: 700 1.55rem/1.25 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .9rem; }
.insight-body  { font: 400 .96rem/1.85 'Inter', sans-serif; color: #7A8278; margin-bottom: 1.3rem; }
.hl-red   { font: 700 1.7rem/1 'Playfair Display', serif; color: #C07040; }
.hl-green { font: 700 1.7rem/1 'Playfair Display', serif; color: #5A9C6E; }
.tag-sec-lbl { font: 500 .64rem/1 'Inter', sans-serif; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 5px; }
.lbl-gap { color: #C07040; }
.lbl-ok  { color: #5A9C6E; }
.tag { display: inline-block; margin: 3px 3px; padding: 3px 9px; border-radius: 20px; font: 400 .7rem/1 'Inter', sans-serif; }
.tag-gap { background: rgba(192,112,64,.10); color: #C07040; border: 1px solid rgba(192,112,64,.22); }
.tag-ok  { background: rgba(90,156,110,.10);  color: #5A9C6E; border: 1px solid rgba(90,156,110,.22); }
.insight-cta   { font: 500 .75rem/1 'Inter', sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #3D6B4F; }
.insight-empty { text-align: center; padding: 2rem; color: #242A38; font: 300 .88rem/1.6 'Inter', sans-serif; }

/* ── Section 1: Narrative ────────────────────────────────── */
.s1-title  { font: 700 3.4rem/1.08 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .85rem; }
.s1-sub    { font: 300 1.05rem/1.85 'Inter', sans-serif; color: #72706A; max-width: 580px; margin-bottom: .5rem; }
.s1-bridge {
    font: 400 1.0rem/1.7 'Inter', sans-serif; color: #C0BCB6;
    padding: 1rem 1.5rem; border-left: 3px solid #3D6B4F;
    border-radius: 0 8px 8px 0; background: rgba(74,124,89,.06);
    margin-bottom: 1.6rem;
}
.s1-bridge em { color: #E2DDD6; font-style: normal; font-weight: 500; }

/* ── Section 1: KPI cards ────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.4rem; }
.kpi-card { background: #10151E; border: 1px solid #1C2230; border-radius: 10px; padding: 1.2rem 1.1rem 1rem; text-align: center; }
.kpi-card.accent-amber { border-color: #4A3210; }
.kpi-card.accent-green { border-color: #1A3828; }
.kpi-val       { font: 700 2.1rem/1 'Playfair Display', serif; color: #C8C4BE; display: block; margin-bottom: .45rem; }
.kpi-val-amber { color: #C9901A !important; }
.kpi-val-green { color: #5A9C6E !important; }
.kpi-label     { font: 500 .75rem/1.3 'Inter', sans-serif; color: #5E626E; display: block; margin-bottom: .3rem; }
.kpi-note      { font: 300 .67rem/1.45 'Inter', sans-serif; color: #2A2E3A; display: block; }

/* ── Section 2: Narrative ────────────────────────────────── */
.s2-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .85rem; }
.s2-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #72706A; max-width: 600px; margin-bottom: .5rem; }

/* ── Section 2: Gap cards ────────────────────────────────── */
.gap-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 1.4rem 0; }
.gap-card { background: #0E1320; border: 1px solid #1C2230; border-radius: 10px; padding: 1.3rem 1.2rem 1.1rem; }
.gap-card.critical { border-color: #3A1E10; }
.gap-icon  { font-size: 1.5rem; display: block; margin-bottom: .55rem; }
.gap-svc   { font: 500 .82rem/1.2 'Inter', sans-serif; color: #9A968E; letter-spacing: .06em; margin-bottom: .55rem; }
.gap-n     { font: 700 2.3rem/1 'Playfair Display', serif; color: #C07040; display: block; margin-bottom: .4rem; }
.gap-n-ok  { color: #5A9C6E !important; }
.gap-sub   { font: 300 .72rem/1.5 'Inter', sans-serif; color: #2A2E3A; }
.gap-ratio { font: 300 .68rem/1 'Inter', sans-serif; color: #3A404F; margin-top: .7rem; padding-top: .7rem; border-top: 1px solid #161B26; }
.gap-ratio b { color: #C07040; }

/* ── Section 3: Narrative ────────────────────────────────── */
.s3-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .85rem; }
.s3-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #72706A; max-width: 600px; margin-bottom: .5rem; }

/* ── Section 4: Narrative + toggles ─────────────────────── */
.s4-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .85rem; }
.s4-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #72706A; max-width: 600px; margin-bottom: .5rem; }
div[data-testid="stRadio"] label { font: 400 .82rem/1 'Inter', sans-serif !important; color: #5E626E !important; }
div[data-testid="stRadio"] > div { gap: 1rem; }
.scenario-callout {
    background: rgba(90,156,110,0.06); border: 1px solid rgba(90,156,110,0.18);
    border-left: 3px solid #3D6B4F; border-radius: 0 8px 8px 0;
    padding: .85rem 1.2rem; font: 300 .82rem/1.65 'Inter', sans-serif;
    color: #3A404F; margin-bottom: 1rem;
}
.scenario-callout b { color: #5A9C6E; font-weight: 500; }

/* ── Section 5: Quote ────────────────────────────────────── */
.quote-wrap { text-align: center; padding: 3.5rem 2rem 2rem; max-width: 720px; margin: 0 auto; }
.quote-mark { font: 400 4rem/1 'Playfair Display', serif; color: rgba(90,156,110,0.25); display: block; margin-bottom: -.5rem; }
.quote-text { font: 400 italic 1.8rem/1.55 'Playfair Display', serif; color: #C8C4BE; margin-bottom: 1.2rem; }
.quote-source { font: 300 .75rem/1 'Inter', sans-serif; color: #2A2E3A; letter-spacing: .10em; text-transform: uppercase; }
.turn-text { font: 300 1.05rem/1.85 'Inter', sans-serif; color: #5E626E; text-align: center; max-width: 520px; margin: 2rem auto 0; }
.turn-text em { color: #5A9C6E; font-style: normal; }

/* ── Section 5: Echo ─────────────────────────────────────── */
.echo-wrap {
    background: rgba(74,124,89,0.04); border: 1px solid rgba(74,124,89,0.12);
    border-radius: 14px; padding: 2.2rem 2.8rem;
    text-align: center; margin: 0 auto; max-width: 680px;
}
.echo-n     { font: 700 5rem/1 'Playfair Display', serif; color: #5A9C6E; display: block; margin-bottom: .6rem; }
.echo-label { font: 300 1.0rem/1.7 'Inter', sans-serif; color: #5E626E; max-width: 440px; margin: 0 auto .8rem; }
.echo-sub   { font: 300 .75rem/1.6 'Inter', sans-serif; color: #2A2E3A; max-width: 400px; margin: 0 auto; }

/* ── Section 5: Identity buttons ─────────────────────────── */
div[data-testid="stButton"] button {
    background: #10151E !important; border: 1px solid #1C2230 !important;
    border-radius: 10px !important; color: #5E626E !important;
    font: 400 .78rem/1.3 'Inter', sans-serif !important;
    height: 72px !important; transition: border-color .2s, background .2s !important;
}
div[data-testid="stButton"] button:hover {
    border-color: rgba(90,156,110,0.40) !important;
    background: rgba(74,124,89,0.05) !important; color: #C8C4BE !important;
}
div[data-testid="stButton"] button:focus,
div[data-testid="stButton"] button:active {
    border-color: rgba(90,156,110,0.70) !important;
    background: rgba(74,124,89,0.08) !important; color: #E2DDD6 !important;
}

/* ── Section 5: Response card ────────────────────────────── */
.response-card {
    background: #0E1320; border: 1px solid #1C2230;
    border-left: 3px solid #3D6B4F; border-radius: 0 12px 12px 0;
    padding: 2rem 2.4rem; margin-top: 1.4rem; max-width: 780px;
}
.response-title { font: 700 1.55rem/1.2 'Playfair Display', serif; color: #E2DDD6; margin-bottom: .7rem; }
.response-body  { font: 300 .92rem/1.85 'Inter', sans-serif; color: #5E626E; margin-bottom: 1.2rem; }
.response-body em { color: #8CC4A0; font-style: italic; }
.response-body b  { color: #9A968E; font-weight: 500; }
.response-actions { display: flex; flex-wrap: wrap; gap: 8px; }
.r-btn {
    font: 400 .72rem/1 'Inter', sans-serif; letter-spacing: .10em; text-transform: uppercase;
    padding: 7px 16px; border-radius: 20px;
    border: 1px solid rgba(90,156,110,0.30); color: #5A9C6E;
    background: rgba(74,124,89,0.06); text-decoration: none; display: inline-block;
}

/* ── Section 5: Final statement ──────────────────────────── */
.final-wrap { text-align: center; padding: 4rem 2rem 2rem; }
.final-you     { font: 300 1.1rem/1 'Inter', sans-serif; letter-spacing: .28em; text-transform: uppercase; color: #2A2E3A; margin-bottom: .6rem; display: block; }
.final-belong  { font: 700 4.2rem/1.1 'Playfair Display', serif; color: #5A9C6E; display: block; margin-bottom: 1.6rem; }
.final-link    { font: 400 .72rem/1 'Inter', sans-serif; letter-spacing: .18em; text-transform: uppercase; color: #3D6B4F; text-decoration: none; border-bottom: 1px solid rgba(90,156,110,0.25); padding-bottom: 2px; display: inline-block; }
.land-ack      { font: 300 italic .75rem/1.8 'Inter', sans-serif; color: #1C2230; max-width: 560px; margin: 3rem auto 0; text-align: center; line-height: 1.85; }

/* ── Credibility badges ───────────────────────────────────── */
.badge-row {
    display: flex; gap: 10px; flex-wrap: wrap;
    margin-bottom: .65rem; align-items: center;
}
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    font: 400 .62rem/1 'Inter', sans-serif;
    letter-spacing: .10em; text-transform: uppercase;
    padding: 4px 10px; border-radius: 20px;
}
.badge-real {
    background: rgba(90,156,110,0.08);
    border: 1px solid rgba(90,156,110,0.25);
    color: #5A9C6E;
}
.badge-sim {
    background: rgba(186,117,23,0.08);
    border: 1px solid rgba(186,117,23,0.22);
    color: #C9901A;
}
.badge-dot {
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}
.badge-real .badge-dot { background: #5A9C6E; }
.badge-sim  .badge-dot { background: #C9901A; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# SHARED CONSTANTS
# Used by Section 0 (card rendering) and Section 5 (callback)
# ════════════════════════════════════════════════════════════════
RESEARCH_GAP_THRESHOLD = 500  # papers; services below this are flagged

SERVICES = {
    "Provisioning": {
        "css": "provisioning",
        "items": [
            {"name": "Biochemicals",        "icon": "🧬", "desc": "Molecules used in medicine",                                   "papers": 11097},
            {"name": "Fibre · Hide · Wood", "icon": "🌲", "desc": "Materials used for clothing or construction",                   "papers": 3538},
            {"name": "Fuel",                "icon": "⚡", "desc": "Materials used to generate energy",                             "papers": 1676},
            {"name": "Potable Water",       "icon": "💧", "desc": "Fresh water that is safe to consume",                           "papers": 784},
            {"name": "Food",                "icon": "🌾", "desc": "Nutritious ingredients from wild & domesticated habitats",      "papers": 439},
            {"name": "Biodiversity",        "icon": "🦋", "desc": "The variety of living species on Earth",                        "papers": 65},
        ]
    },
    "Cultural": {
        "css": "cultural",
        "items": [
            {"name": "Inspiration · Education", "icon": "🎨", "desc": "Art, science, music, literature, and design",                "papers": 679},
            {"name": "Aesthetic",               "icon": "🌸", "desc": "Mental and physical benefits of natural beauty",             "papers": 621},
            {"name": "Recreation",              "icon": "🏕️", "desc": "Physical and mental health from nature experiences",         "papers": 260},
            {"name": "Cultural Heritage",       "icon": "🏛️", "desc": "Societal value placed upon landscapes",                      "papers": 34},
            {"name": "Spiritual",               "icon": "🕊️", "desc": "Support for the spiritual lives of people",                  "papers": 0},
            {"name": "Cultural Identity",       "icon": "🌍", "desc": "Individual and societal identity from human-nature bonds",   "papers": 0},
        ]
    },
    "Regulating": {
        "css": "regulating",
        "items": [
            {"name": "Disease Regulation",   "icon": "🦠", "desc": "Natural systems reducing disease and disease vectors",        "papers": 4418},
            {"name": "Waste Treatment",      "icon": "♻️", "desc": "Filtering and treating organic and chemical waste",            "papers": 2913},
            {"name": "Climate Regulation",   "icon": "🌡️", "desc": "Stabilization of climatic conditions",                        "papers": 854},
            {"name": "Atmospheric Reg.",     "icon": "💨", "desc": "Production and consumption of essential molecules (O₂)",      "papers": 847},
            {"name": "Water Regulation",     "icon": "🌊", "desc": "Timing and volume of water distribution across land",         "papers": 716},
            {"name": "Pollination",          "icon": "🐝", "desc": "Distribution of pollen seeds for plant reproduction",         "papers": 355},
            {"name": "Coastline Regulation", "icon": "🏖️", "desc": "Stabilization of coastal lands via mangroves and reefs",     "papers": 146},
        ]
    },
    "Supporting": {
        "css": "supporting",
        "items": [
            {"name": "Primary Production", "icon": "☀️", "desc": "Creation of sugars from sunlight — base of all food chains",  "papers": 718},
            {"name": "Soil Formation",     "icon": "🌱", "desc": "The ongoing creation of new fertile soil",                     "papers": 343},
            {"name": "Nutrient Cycling",   "icon": "🔄", "desc": "The movement of nutrients through ecosystems",                 "papers": 58},
        ]
    }
}


# ════════════════════════════════════════════════════════════════
# SESSION STATE  (initialised once at app startup)
# Covers: Section 0 checkbox keys + Section 5 identity key
# ════════════════════════════════════════════════════════════════
_svc_names = [s["name"] for cat in SERVICES.values() for s in cat["items"]]
for _name in _svc_names:
    if _name not in st.session_state:
        st.session_state[_name] = False

if "identity" not in st.session_state:
    st.session_state.identity = None


# ════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════
def section_sep():
    """Thin horizontal rule used between all six sections."""
    st.markdown(
        '<div class="section-sep"></div>',
        unsafe_allow_html=True,
    )

def credibility_badge(has_real: bool = True, has_sim: bool = False):
    """
    Renders a small badge row above any chart indicating whether the
    data shown is directly reported by Jacobs et al. (2025) or simulated.

    Parameters
    ----------
    has_real : bool  — show the 'Real data' badge
    has_sim  : bool  — show the 'Simulated' badge
    """
    badges = ""
    if has_real:
        badges += (
            '<span class="badge badge-real">'
            '<span class="badge-dot"></span>'
            'Real data · Jacobs et al. (2025)</span>'
        )
    if has_sim:
        badges += (
            '<span class="badge badge-sim">'
            '<span class="badge-dot"></span>'
            'Simulated / illustrative</span>'
        )
    st.markdown(
        f'<div class="badge-row">{badges}</div>',
        unsafe_allow_html=True,
    )

def build_sankey(replace, enhance, support, label_r, label_e, label_s):
    """
    Build and return a Plotly Sankey figure for Section 4.
    Nodes: Replace | Enhance | Support → 6 service buckets
    """
    r_bio  = int(replace * 0.48); r_dis  = int(replace * 0.17)
    r_was  = int(replace * 0.15); r_fib  = int(replace * 0.11)
    r_crit = int(replace * 0.01)
    r_oth  = replace - r_bio - r_dis - r_was - r_fib - r_crit

    e_bio  = int(enhance * 0.44); e_fib  = int(enhance * 0.14)
    e_was  = int(enhance * 0.09); e_dis  = int(enhance * 0.09)
    e_crit = int(enhance * 0.02)
    e_oth  = enhance - e_bio - e_fib - e_was - e_dis - e_crit

    s_bio  = int(support * 0.31)
    s_crit = int(support * 0.35)
    s_oth  = support - s_bio - s_crit

    nodes = [
        label_r, label_e, label_s,
        "Biochemicals", "Disease Regulation", "Waste Treatment",
        "Fibre / Materials", "Other Services",
        "Critical Services\n(Pollination · Soil · Nutrients)",
    ]
    node_colors = [
        "rgba(186,117,23,0.85)", "rgba(29,158,117,0.80)", "rgba(74,158,219,0.85)",
        "rgba(58,64,79,0.90)",   "rgba(58,64,79,0.85)",   "rgba(58,64,79,0.85)",
        "rgba(58,64,79,0.85)",   "rgba(40,46,58,0.80)",   "rgba(90,156,110,0.90)",
    ]
    source = [0,0,0,0,0,0, 1,1,1,1,1,1, 2,2,2]
    target = [3,4,5,6,7,8, 3,4,5,6,7,8, 3,7,8]
    value  = [
        r_bio, r_dis, r_was, r_fib, r_oth, r_crit,
        e_bio, e_dis, e_was, e_fib, e_oth, e_crit,
        s_bio, s_oth, s_crit,
    ]
    link_colors = []
    for s, t in zip(source, target):
        if t == 8:
            link_colors.append("rgba(90,156,110,0.55)" if s == 2 else "rgba(90,156,110,0.18)")
        elif s == 0: link_colors.append("rgba(186,117,23,0.18)")
        elif s == 1: link_colors.append("rgba(29,158,117,0.18)")
        else:        link_colors.append("rgba(74,158,219,0.22)")

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(pad=18, thickness=22, label=nodes, color=node_colors,
                  line=dict(color="#0A0E14", width=0.5)),
        link=dict(source=source, target=target, value=value, color=link_colors,
                  hovertemplate="%{source.label} → %{target.label}<br>Flow: %{value} units<extra></extra>"),
    ))
    fig.update_layout(
        paper_bgcolor="#0A0E14",
        font=dict(size=11, color="#5E626E", family="Inter, sans-serif"),
        height=440, margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig


# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 0 · Feel — Before You Read a Single Number
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

st.markdown('<div class="hero-eyebrow">Manufactured Ecosystems · Research Dashboard</div>',
            unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Nature Is Not Optional.</h1>',
            unsafe_allow_html=True)
st.markdown("""
<p class="hero-sub">
    Over 68,000 scientific papers. Twenty years of research.<br>
    One urgent question: <em>can technology replace what nature provides?</em><br><br>
    Before we show you the data, we want to ask something about your day.
</p>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero-prompt">
    <strong>Look at the 22 services nature provides below.</strong>
    Select every one you have already relied on since you woke up this morning —
    even without thinking about it.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone B: Service cards grid ────────────────────────────────
for cat_name, cat_data in SERVICES.items():
    css = cat_data["css"]
    st.markdown(f'<div class="cat-pill cp-{css}">{cat_name} Services</div>',
                unsafe_allow_html=True)
    items = cat_data["items"]
    rows  = [items[i : i + 3] for i in range(0, len(items), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, svc in zip(cols, row):
            name = svc["name"]
            with col:
                is_selected = st.session_state.get(name, False)
                card_cls    = f"svc-sel-{css}" if is_selected else ""
                st.markdown(f"""
                <div class="svc-card {card_cls}">
                    <span class="svc-icon">{svc['icon']}</span>
                    <div class="svc-name">{name}</div>
                    <div class="svc-desc">{svc['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.checkbox("I relied on this today", key=name)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone C: Live counter ──────────────────────────────────────
_s0_selected = [
    svc for cat in SERVICES.values() for svc in cat["items"]
    if st.session_state.get(svc["name"], False)
]
_n0 = len(_s0_selected)
st.markdown(f"""
<div class="ctr">
    <div class="ctr-n">{_n0}</div>
    <div class="ctr-sub">
        {"service selected" if _n0 == 1 else "services selected"}
        &nbsp;·&nbsp; of 22 total ecosystem services
    </div>
</div>
""", unsafe_allow_html=True)

# ── Zone D: Personalised insight panel ───────────────────────
if _n0 == 0:
    st.markdown("""
    <div class="insight-empty">
        ↑ Select at least one service above to reveal your personalized data insight.
    </div>
    """, unsafe_allow_html=True)
else:
    _gap0 = [s for s in _s0_selected if s["papers"] < RESEARCH_GAP_THRESHOLD]
    _ok0  = [s for s in _s0_selected if s["papers"] >= RESEARCH_GAP_THRESHOLD]
    _ngap0 = len(_gap0)

    if _ngap0 == 0:
        _body0 = (
            f'All <span class="hl-green">{_n0}</span> services you selected are '
            f'relatively well-represented in bio-inspired research. '
            f"Scroll down — you'll see that many other services people depend on are not so fortunate."
        )
    elif _ngap0 == _n0:
        _body0 = (
            f'Every one of the <span class="hl-red">{_n0}</span> services '
            f'you rely on today has fewer than {RESEARCH_GAP_THRESHOLD:,} bio-inspired research papers. '
            f'Science is building technological backups — just not yet for the things '
            f'<em>you</em> need most.'
        )
    else:
        _body0 = (
            f'Of the <span class="hl-green">{_n0}</span> services you depend on today, '
            f'<span class="hl-red">{_ngap0}</span> '
            f'{"has" if _ngap0 == 1 else "have"} fewer than {RESEARCH_GAP_THRESHOLD:,} '
            f'bio-inspired research papers. '
            f'If those services fail, very few technological backup plans currently exist.'
        )

    _gap_tags0 = "".join(
        f'<span class="tag tag-gap">{s["icon"]} {s["name"]}</span>' for s in _gap0
    )
    _ok_tags0 = "".join(
        f'<span class="tag tag-ok">{s["icon"]} {s["name"]}</span>' for s in _ok0
    )
    _gap_block0 = (
        f'<div style="margin-bottom:.9rem">'
        f'<div class="tag-sec-lbl lbl-gap">Research gap — fewer than {RESEARCH_GAP_THRESHOLD:,} papers ({_ngap0})</div>'
        f'{_gap_tags0}</div>'
    ) if _gap0 else ""
    _ok_block0 = (
        f'<div style="margin-bottom:1.4rem">'
        f'<div class="tag-sec-lbl lbl-ok">Better researched ({len(_ok0)})</div>'
        f'{_ok_tags0}</div>'
    ) if _ok0 else ""

    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">What the research says about your day.</div>
        <div class="insight-body">{_body0}</div>
        {_gap_block0}
        {_ok_block0}
        <div class="insight-cta">↓ &nbsp; Scroll to see what 20 years of global research actually looks like</div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 1 · Discovery — 68,972 Attempts
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

section_sep()

st.markdown('<div class="s1-eyebrow">Section 01 · Discovery</div>', unsafe_allow_html=True)
st.markdown('<h2 class="s1-title">68,972 Attempts.</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="s1-sub">
    For twenty years, the global scientific community has been working on
    something unprecedented: learning from nature in order to engineer it.
    68,972 published papers. Hundreds of research groups. A shared, if often
    unspoken, question —
    <em style="color:#C0BCB6; font-style:italic">
    what happens when the natural world can no longer do this on its own?</em>
</p>
<p class="s1-sub">Before we show you the gaps, here is the scale of the effort.</p>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone B: KPI cards ─────────────────────────────────────────
st.markdown("""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-val">59,651</span>
    <span class="kpi-label">Papers analyzed</span>
    <span class="kpi-note">Bio-inspired research corpus<br>Web of Science, 2004–2025</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-val">20 / 22</span>
    <span class="kpi-label">Services engaged</span>
    <span class="kpi-note">Spiritual &amp; Cultural Identity<br>remain entirely out of reach</span>
  </div>
  <div class="kpi-card accent-amber">
    <span class="kpi-val kpi-val-amber">58%</span>
    <span class="kpi-label">Aim to replace nature</span>
    <span class="kpi-note">The dominant paradigm —<br>stand-alone substitutes for ES</span>
  </div>
  <div class="kpi-card accent-green">
    <span class="kpi-val kpi-val-green">3%</span>
    <span class="kpi-label">Aim to support nature</span>
    <span class="kpi-note">The most ecologically aligned<br>approach, yet heavily marginalized</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Zone C: Particle animation — Option B (three streams) ────
# Canvas is divided into three vertical zones proportional to
# the real data: Replace 58% | Enhance 39% | Support 3%
# Soft visual separators + percentage labels make the proportion
# immediately readable without any prior knowledge.
_particle_html = """
<div style="width:100%;height:280px;background:#0E1320;position:relative;
            overflow:hidden;border-radius:12px;border:1px solid #1C2230;">

  <canvas id="particleCanvas"
    style="display:block;position:absolute;top:0;left:0;width:100%;height:100%;"></canvas>

  <!-- Zone labels (rendered above canvas via z-index) -->
  <div style="position:absolute;top:0;left:0;width:100%;height:100%;
              pointer-events:none;display:flex;">

    <!-- Replace zone: 58% -->
    <div style="width:58%;display:flex;flex-direction:column;
                justify-content:flex-start;align-items:center;padding-top:18px;
                border-right:1px solid rgba(200,196,188,0.07);">
      <span style="font-family:Georgia,serif;font-size:22px;font-weight:700;
                   color:rgba(184,134,11,0.85);line-height:1;">58%</span>
      <span style="font-family:Inter,sans-serif;font-size:10px;font-weight:400;
                   color:rgba(184,134,11,0.45);letter-spacing:.12em;
                   text-transform:uppercase;margin-top:4px;">Replace</span>
    </div>

    <!-- Enhance zone: 39% -->
    <div style="width:39%;display:flex;flex-direction:column;
                justify-content:flex-start;align-items:center;padding-top:18px;
                border-right:1px solid rgba(200,196,188,0.07);">
      <span style="font-family:Georgia,serif;font-size:22px;font-weight:700;
                   color:rgba(29,158,117,0.85);line-height:1;">39%</span>
      <span style="font-family:Inter,sans-serif;font-size:10px;font-weight:400;
                   color:rgba(29,158,117,0.45);letter-spacing:.12em;
                   text-transform:uppercase;margin-top:4px;">Enhance</span>
    </div>

    <!-- Support zone: 3% -->
    <div style="width:3%;display:flex;flex-direction:column;
                justify-content:flex-start;align-items:center;padding-top:18px;">
      <span style="font-family:Georgia,serif;font-size:13px;font-weight:700;
                   color:rgba(74,158,219,0.85);line-height:1;">3%</span>
      <span style="font-family:Inter,sans-serif;font-size:8px;font-weight:400;
                   color:rgba(74,158,219,0.45);writing-mode:vertical-rl;
                   letter-spacing:.10em;text-transform:uppercase;margin-top:6px;">
        Support
      </span>
    </div>
  </div>

  <!-- Bottom caption -->
  <div style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);
              text-align:center;pointer-events:none;">
    <span style="font-family:Georgia,serif;font-size:14px;font-weight:700;
                 color:rgba(226,221,214,0.70);">
      31,593 papers. Each one a choice.
    </span>
  </div>
</div>

<script>
(function() {
  const canvas = document.getElementById('particleCanvas');
  const ctx    = canvas.getContext('2d');

  function resize() {
    canvas.width  = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Zone boundaries (proportional to canvas width)
  const ZONES = [
    { xMin: 0.000, xMax: 0.580, color: '#B8860B', label: 'Replace'  },  // 58%
    { xMin: 0.580, xMax: 0.970, color: '#1D9E75', label: 'Enhance'  },  // 39%
    { xMin: 0.970, xMax: 1.000, color: '#2E6B8A', label: 'Support'  },  //  3%
  ];

  class Particle {
    constructor(initY) { this.init(initY); }
    init(initY) {
      // Pick zone randomly — zone width already encodes the proportion
      const zone    = ZONES[Math.floor(Math.random() * ZONES.length)];
      const zW      = zone.xMax - zone.xMin;
      this.x        = (zone.xMin + Math.random() * zW) * canvas.width;
      this.y        = initY ? Math.random() * canvas.height : -6;
      this.size     = Math.random() * 2.0 + 0.8;
      this.speedY   = Math.random() * 1.1 + 0.5;
      this.opacity  = Math.random() * 0.50 + 0.15;
      this.color    = zone.color;
    }
    update() {
      this.y += this.speedY;
      if (this.y > canvas.height + 10) this.init(false);
    }
    draw() {
      ctx.globalAlpha = this.opacity;
      ctx.fillStyle   = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // More particles in the Replace zone, fewer in Support —
  // achieved naturally because zone widths are proportional.
  // We use a flat count; distribution emerges from zone width.
  const particles = Array.from({ length: 420 }, () => new Particle(true));

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
"""
components.html(_particle_html, height=290)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Bridge sentence ───────────────────────────────────────────
st.markdown("""
<div class="s1-bridge">
    This imbalance is not a recent development.
    <em>It has been building for twenty years</em> — and accelerating
    as the climate crisis intensifies the demand for technological solutions.
</div>
""", unsafe_allow_html=True)

# ── Zone D: Stacked area chart ────────────────────────────────
st.markdown('<div class="chart-label">Biomimetic design paradigms · 2004 – 2025</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)
np.random.seed(42)
_years = list(range(2004, 2026))
_raw_w = np.array([
    0.80, 1.00, 1.30, 1.70, 2.20, 2.80, 3.50, 4.30,
    5.20, 6.00, 6.80, 7.50, 8.00, 8.50, 9.00, 9.50,
    10.0, 10.5, 11.0, 11.5, 11.8, 4.50,
])
_base  = (_raw_w / _raw_w.sum() * 31593).astype(int)
_noise = np.random.uniform(0.94, 1.06, len(_years))
_base  = np.maximum((_base * _noise).astype(int), 5)
_r_frac = np.random.uniform(0.55, 0.61, len(_years))
_s_frac = np.random.uniform(0.026, 0.034, len(_years))
_replace_data = (_base * _r_frac).astype(int)
_support_data = np.maximum((_base * _s_frac).astype(int), 3)
_enhance_data = _base - _replace_data - _support_data

_area_fig = go.Figure()
_area_fig.add_trace(go.Scatter(
    x=_years, y=_support_data, name="Support  (3%)", mode="lines",
    line=dict(width=0.8, color="#2E6B8A"), fillcolor="rgba(74,158,219,0.65)",
    stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Support: %{y:,} papers<extra></extra>",
))
_area_fig.add_trace(go.Scatter(
    x=_years, y=_enhance_data, name="Enhance  (39%)", mode="lines",
    line=dict(width=0.8, color="#1D9E75"), fillcolor="rgba(29,158,117,0.50)",
    stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Enhance: %{y:,} papers<extra></extra>",
))
_area_fig.add_trace(go.Scatter(
    x=_years, y=_replace_data, name="Replace  (58%)", mode="lines",
    line=dict(width=0.8, color="#BA7517"), fillcolor="rgba(186,117,23,0.60)",
    stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Replace: %{y:,} papers<extra></extra>",
))
_area_fig.add_vline(x=2013, line_dash="dot",
                    line_color="rgba(200,196,188,0.15)", line_width=1.2)
_area_fig.add_annotation(
    x=2013.25, y=0.97, yref="paper",
    text='Fitter (2013):<br>"Can ES be replaced?"',
    font=dict(size=9, color="#3A404F", family="Inter, sans-serif"),
    showarrow=False, xanchor="left", yanchor="top",
)
_area_fig.add_annotation(
    x=2021, y=int(_support_data[_years.index(2021)]),
    text="<b>Support: 3%</b><br>Most needed. Least resourced.",
    font=dict(size=10, color="#4A9EDB", family="Inter, sans-serif"),
    showarrow=True, arrowhead=2, arrowcolor="#4A9EDB", arrowwidth=1.2,
    ax=90, ay=-55,
    bgcolor="rgba(10,14,20,0.88)", bordercolor="rgba(74,158,219,0.28)",
    borderwidth=1, borderpad=6,
)
_area_fig.update_layout(
    paper_bgcolor="#0A0E14", plot_bgcolor="#0E1320",
    height=430, margin=dict(l=65, r=25, t=25, b=55),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#0E1320", bordercolor="#1C2230",
                    font=dict(size=11, color="#C8C4BE", family="Inter, sans-serif")),
    legend=dict(orientation="h", y=1.03, x=0.99, xanchor="right", yanchor="bottom",
                font=dict(size=11, color="#6A6E78", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", traceorder="reversed"),
    xaxis=dict(tickmode="linear", dtick=2, tickfont=dict(size=11, color="#3A404F"),
               gridcolor="#141A26", linecolor="#1C2230", zeroline=False),
    yaxis=dict(title=dict(text="ES-linked publications per year (simulated)",
                          font=dict(size=11, color="#3A404F")),
               tickfont=dict(size=11, color="#3A404F"), tickformat=",",
               gridcolor="#141A26", linecolor="#1C2230", zeroline=False),
)
st.plotly_chart(_area_fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#20242E;margin-top:.6rem;padding-left:2px;">
    Annual counts modelled from cumulative totals in Jacobs et al. (2025).
    Category proportions — Replace 58%, Enhance 39%, Support 3% — drawn directly from published findings.
    Year-to-year noise (±6%) is simulated for illustration.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#2A3840;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 2 · The Gap Map — The Services Nobody Is Building
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

section_sep()

st.markdown('<div class="s2-eyebrow">Section 02 · The Gap Map</div>', unsafe_allow_html=True)
st.markdown('<h2 class="s2-title">The Services Nobody Is Building.</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="s2-sub">
    Of the 22 ecosystem services that sustain life on Earth,
    bio-inspired research has touched 20. But engagement is not the same as
    investment. The map below shows where science is concentrating its effort —
    and where the foundations of our food system, our water cycle, and our
    cultural identity are being left almost entirely unaddressed.
</p>
<p class="s2-sub">
    Each tile's area is proportional to publication count.
    Hover over any tile to see the Replace / Enhance / Support breakdown.
    Click a category to zoom in; click the breadcrumb to return.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────
# fmt: off
_RAW2 = [
    ("Biochemicals",          "Provisioning", 11097, 0.48, 0.49, 0.03),
    ("Fibre / Hide / Wood",   "Provisioning",  3538, 0.55, 0.42, 0.03),
    ("Fuel",                  "Provisioning",  1676, 0.62, 0.35, 0.03),
    ("Potable Water",         "Provisioning",   784, 0.55, 0.40, 0.05),
    ("Food",                  "Provisioning",   439, 0.62, 0.33, 0.05),
    ("Biodiversity",          "Provisioning",    65, 0.25, 0.45, 0.30),
    ("Disease Regulation",    "Regulating",    4418, 0.72, 0.25, 0.03),
    ("Waste Treatment",       "Regulating",    2913, 0.65, 0.32, 0.03),
    ("Climate Regulation",    "Regulating",     854, 0.48, 0.48, 0.04),
    ("Atmospheric Reg.",      "Regulating",     847, 0.50, 0.45, 0.05),
    ("Water Regulation",      "Regulating",     716, 0.45, 0.48, 0.07),
    ("Pollination",           "Regulating",     355, 0.35, 0.45, 0.20),
    ("Coastline Regulation",  "Regulating",     146, 0.40, 0.50, 0.10),
    ("Primary Production",    "Supporting",     718, 0.35, 0.52, 0.13),
    ("Soil Formation",        "Supporting",     343, 0.30, 0.50, 0.20),
    ("Nutrient Cycling",      "Supporting",      58, 0.20, 0.55, 0.25),
    ("Inspiration/Education", "Cultural",        679, 0.15, 0.45, 0.40),
    ("Aesthetic",             "Cultural",        621, 0.20, 0.50, 0.30),
    ("Recreation",            "Cultural",        260, 0.15, 0.55, 0.30),
    ("Cultural Heritage",     "Cultural",         34, 0.10, 0.50, 0.40),
    ("Spiritual",             "Cultural",          0, 0.00, 0.00, 0.00),
    ("Cultural Identity",     "Cultural",          0, 0.00, 0.00, 0.00),
]
# fmt: on

_df2 = pd.DataFrame(_RAW2, columns=["service","category","total","repl_pct","enha_pct","supp_pct"])
_df2["replace"] = (_df2["total"] * _df2["repl_pct"]).round().astype(int)
_df2["enhance"] = (_df2["total"] * _df2["enha_pct"]).round().astype(int)
_df2["support"] = (_df2["total"] - _df2["replace"] - _df2["enhance"]).clip(lower=0)
_df2["adj"]     = _df2["total"].clip(lower=1)
_df2_sorted     = _df2.sort_values("total", ascending=True).reset_index(drop=True)

# ── Zone B: Treemap ───────────────────────────────────────────
st.markdown('<div class="chart-label">Coverage across all 22 ecosystem services</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)

# Improvement #3: interaction tip above treemap
st.markdown("""
<div style="display:inline-flex;align-items:center;gap:8px;
            background:rgba(74,124,89,0.06);border:1px solid rgba(74,124,89,0.15);
            border-radius:6px;padding:6px 14px;
            font:300 .72rem/1 'Inter',sans-serif;color:#3D6B4F;margin-bottom:.8rem;">
    💡 &nbsp; Click any category tile to zoom in — then click the breadcrumb bar to return.
</div>
""", unsafe_allow_html=True)

_CAT_PAL2 = {
    "Provisioning": {"cat": "#C9901A", "svc": "rgba(201,144,26,0.45)"},
    "Regulating":   {"cat": "#1D9E75", "svc": "rgba(29,158,117,0.40)"},
    "Supporting":   {"cat": "#5A9C6E", "svc": "rgba(90,156,110,0.45)"},
    "Cultural":     {"cat": "#7F77DD", "svc": "rgba(127,119,221,0.42)"},
}
_MISSING_CLR = "#141A26"

_ids2, _lbl2, _par2, _val2, _col2, _hov2 = [], [], [], [], [], []
_ids2.append("root"); _lbl2.append("All Ecosystem Services"); _par2.append("")
_val2.append(0); _col2.append("#0A0E14"); _hov2.append("")

for _cat, _pal in _CAT_PAL2.items():
    _real = int(_df2[_df2["category"] == _cat]["total"].sum())
    _nsvc = len(_df2[_df2["category"] == _cat])
    _ids2.append(f"cat_{_cat}"); _lbl2.append(_cat); _par2.append("root")
    _val2.append(0); _col2.append(_pal["cat"])
    _hov2.append(f"<b>{_cat}</b><br>Total papers: {_real:,}<br>Services: {_nsvc}")

for _, _row in _df2.iterrows():
    _empty = (_row["total"] == 0)
    _sid = "svc_" + _row["service"].replace("/","_").replace(" ","_").replace(".","")
    if _empty:
        _htxt = (f"<b>{_row['service']}</b><br>"
                 "<span style='color:#3A404F;'>No bio-inspired research found.</span>")
    else:
        _htxt = (f"<b>{_row['service']}</b><br>Total: {_row['total']:,} papers<br>"
                 f"<span style='color:#BA7517;'>Replace: {_row['replace']:,} ({_row['repl_pct']*100:.0f}%)</span><br>"
                 f"<span style='color:#1D9E75;'>Enhance: {_row['enhance']:,} ({_row['enha_pct']*100:.0f}%)</span><br>"
                 f"<span style='color:#4A9EDB;'>Support: {_row['support']:,} ({_row['supp_pct']*100:.0f}%)</span>")
    _ids2.append(_sid); _lbl2.append(_row["service"]); _par2.append(f"cat_{_row['category']}")
    _val2.append(int(_row["adj"]))
    _col2.append(_MISSING_CLR if _empty else _CAT_PAL2[_row["category"]]["svc"])
    _hov2.append(_htxt)

_tree_fig = go.Figure(go.Treemap(
    ids=_ids2, labels=_lbl2, parents=_par2, values=_val2,
    branchvalues="remainder",
    customdata=_hov2, hovertemplate="%{customdata}<extra></extra>",
    marker=dict(colors=_col2, line=dict(width=2, color="#0A0E14"),
                pad=dict(t=24, l=4, r=4, b=4)),
    textfont=dict(size=11, color="#E2DDD6", family="Inter, sans-serif"),
    textinfo="label", tiling=dict(packing="squarify", pad=2),
    maxdepth=2, root_color="#0A0E14",
))
_tree_fig.update_layout(paper_bgcolor="#0A0E14", height=520,
                        margin=dict(l=0, r=0, t=8, b=8))
st.plotly_chart(_tree_fig, use_container_width=True, config={"displayModeBar": False})

# ── Zone C: Gap callout cards ─────────────────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">The critical gap — food system services</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)

st.markdown("""
<p class="chart-sub-label">
    Pollination, soil formation, and nutrient cycling collectively underpin
    global food security. Together they account for just 756 papers —
    fewer than 7% of what a single service (Biochemicals) has attracted.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="gap-grid">
  <div class="gap-card">
    <span class="gap-icon">🧬</span>
    <div class="gap-svc">Biochemicals</div>
    <span class="gap-n gap-n-ok">11,097</span>
    <div class="gap-sub">Molecules used in medicine. The single most-studied ES in the
        bio-inspired corpus. Strong commercial incentives drive this concentration.</div>
    <div class="gap-ratio">Reference service</div>
  </div>
  <div class="gap-card critical">
    <span class="gap-icon">🐝</span>
    <div class="gap-svc">Pollination</div>
    <span class="gap-n">355</span>
    <div class="gap-sub">Responsible for 75% of global food crop varieties.
        RoboBee can physically pollinate — but cannot replace a bee's role in the food chain above it.</div>
    <div class="gap-ratio"><b>1 paper</b> for every 31 in Biochemicals</div>
  </div>
  <div class="gap-card critical">
    <span class="gap-icon">🔄</span>
    <div class="gap-svc">Nutrient Cycling</div>
    <span class="gap-n">58</span>
    <div class="gap-sub">The movement of nitrogen, phosphorus, and carbon through living systems.
        The rarest research topic in the entire 59,651-paper corpus.</div>
    <div class="gap-ratio"><b>1 paper</b> for every 191 in Biochemicals</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Zone D: Sorted horizontal bar ────────────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Full coverage index — all 22 services</div>',
            unsafe_allow_html=True)
st.markdown("""
<p class="chart-sub-label">
    Sorted by total bio-inspired publication count.
    The five services at the top represent 78% of all ES-linked research.
    The five at the bottom represent less than 0.5%.
</p>
""", unsafe_allow_html=True)

_bar2 = go.Figure()
_bar2.add_trace(go.Bar(name="Replace", y=_df2_sorted["service"], x=_df2_sorted["replace"],
    orientation="h", marker=dict(color="rgba(186,117,23,0.72)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Replace: %{x:,} papers<extra></extra>"))
_bar2.add_trace(go.Bar(name="Enhance", y=_df2_sorted["service"], x=_df2_sorted["enhance"],
    orientation="h", marker=dict(color="rgba(29,158,117,0.65)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Enhance: %{x:,} papers<extra></extra>"))
_bar2.add_trace(go.Bar(name="Support", y=_df2_sorted["service"], x=_df2_sorted["support"],
    orientation="h", marker=dict(color="rgba(74,158,219,0.80)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Support: %{x:,} papers<extra></extra>"))
_bar2.add_annotation(
    x=_df2_sorted[_df2_sorted["service"] == "Biochemicals"]["total"].values[0],
    y="Biochemicals", text="  11,097 papers",
    font=dict(size=10, color="#5E626E", family="Inter, sans-serif"),
    showarrow=False, xanchor="left")
_bar2.add_annotation(
    x=62, y="Nutrient Cycling", text="  58 papers — rarest in corpus",
    font=dict(size=10, color="#C07040", family="Inter, sans-serif"),
    showarrow=False, xanchor="left")
_bar2.update_layout(
    barmode="stack", paper_bgcolor="#0A0E14", plot_bgcolor="#0E1320",
    height=640, margin=dict(l=10, r=140, t=20, b=55),
    hovermode="y unified",
    hoverlabel=dict(bgcolor="#0E1320", bordercolor="#1C2230",
                    font=dict(size=11, color="#C8C4BE", family="Inter, sans-serif")),
    legend=dict(orientation="h", y=1.02, x=0.99, xanchor="right", yanchor="bottom",
                font=dict(size=11, color="#6A6E78", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", traceorder="normal"),
    xaxis=dict(title=dict(text="Bio-inspired publications (real counts, Jacobs et al. 2025)",
                          font=dict(size=11, color="#3A404F")),
               tickfont=dict(size=11, color="#3A404F"), tickformat=",",
               gridcolor="#141A26", linecolor="#1C2230", zeroline=False),
    yaxis=dict(tickfont=dict(size=10, color="#5E626E", family="Inter, sans-serif"),
               linecolor="#1C2230", gridcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(_bar2, use_container_width=True, config={"displayModeBar": False})

st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#20242E;margin-top:.4rem;padding-left:2px;">
    Total paper counts drawn from Figure 3 of Jacobs et al. (2025).
    Replace / Enhance / Support splits within each service are simulated.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#2A3840;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 3 · Islands of Expertise — Why Does the Gap Exist?
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

section_sep()

st.markdown('<div class="s3-eyebrow">Section 03 · Islands of Expertise</div>',
            unsafe_allow_html=True)
st.markdown('<h2 class="s3-title">Why Does the Gap Exist?</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="s3-sub">
    The uneven distribution of bio-inspired research is not accidental.
    It reflects a structural reality: the disciplines most likely to build
    technological substitutes for nature are not talking to the disciplines
    that understand what nature is actually doing.
</p>
<p class="s3-sub">
    The network below maps the academic communities publishing in biomimetics
    and bio-inspired design. Two clusters emerge with striking clarity —
    and the bridges between them are almost invisible.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────
_NODES3 = {
    # name: (x, y, size, paradigm, cluster, papers_label)
    "Materials Science":   (-0.68,  0.18, 75, "Replace", "Engineering", "~8,200 papers"),
    "Mech. Engineering":   (-0.52, -0.22, 65, "Replace", "Engineering", "~6,800 papers"),
    "Chemistry":           (-0.84, -0.12, 60, "Replace", "Engineering", "~6,100 papers"),
    "Robotics":            (-0.44, -0.48, 40, "Replace", "Engineering", "~3,900 papers"),
    "Biomedical Eng.":     (-0.62,  0.48, 52, "Replace", "Engineering", "~5,200 papers"),
    "Nanotechnology":      (-0.88,  0.36, 36, "Replace", "Engineering", "~3,400 papers"),
    "Environmental Sci.":  ( 0.72,  0.22, 46, "Enhance", "Ecology",     "~4,400 papers"),
    "Ecology":             ( 0.82, -0.12, 32, "Support", "Ecology",     "~2,900 papers"),
    "Biology":             ( 0.56, -0.38, 36, "Support", "Ecology",     "~3,300 papers"),
    "Conservation Bio.":   ( 0.92, -0.48, 18, "Support", "Ecology",     "~1,400 papers"),
    "Agriculture":         ( 0.62,  0.50, 22, "Enhance", "Ecology",     "~1,900 papers"),
    "Architecture/Design": (-0.08, -0.40, 22, "Enhance", "Bridge",      "~1,800 papers"),
    "Computer Science":    (-0.14,  0.44, 30, "Replace", "Bridge",      "~2,700 papers"),
}

_EDGES3 = [
    ("Materials Science",  "Mech. Engineering",  0.82),
    ("Materials Science",  "Chemistry",           0.76),
    ("Materials Science",  "Nanotechnology",      0.68),
    ("Mech. Engineering",  "Robotics",            0.62),
    ("Mech. Engineering",  "Biomedical Eng.",     0.55),
    ("Chemistry",          "Biomedical Eng.",     0.58),
    ("Nanotechnology",     "Biomedical Eng.",     0.50),
    ("Nanotechnology",     "Chemistry",           0.60),
    ("Ecology",            "Biology",             0.78),
    ("Environmental Sci.", "Ecology",             0.70),
    ("Environmental Sci.", "Agriculture",         0.55),
    ("Biology",            "Conservation Bio.",   0.62),
    ("Ecology",            "Conservation Bio.",   0.48),
    ("Computer Science",   "Mech. Engineering",   0.40),
    ("Computer Science",   "Robotics",            0.45),
    ("Architecture/Design","Mech. Engineering",   0.20),
    ("Architecture/Design","Environmental Sci.",  0.18),
    ("Biology",            "Materials Science",   0.06),
    ("Ecology",            "Mech. Engineering",   0.04),
    ("Environmental Sci.", "Chemistry",           0.08),
    ("Biology",            "Biomedical Eng.",     0.10),
    ("Conservation Bio.",  "Architecture/Design", 0.07),
]

_PAR_COLORS3 = {
    "Replace": "rgba(186,117,23,0.90)",
    "Enhance": "rgba(29,158,117,0.85)",
    "Support": "rgba(74,158,219,0.88)",
}
_PAR_BORDER3 = {
    "Replace": "#C9901A",
    "Enhance": "#1D9E75",
    "Support": "#4A9EDB",
}

# ── Zone B: Network graph ─────────────────────────────────────
st.markdown('<div class="chart-label">Disciplinary co-occurrence network · biomimetics corpus</div>',
            unsafe_allow_html=True)

credibility_badge(has_real=False, has_sim=True)
st.markdown("""
<p class="chart-sub-label">
    Node size = relative publication volume.
    Node colour = dominant design paradigm
    (<span style="color:#C9901A;">replace</span> /
    <span style="color:#1D9E75;">enhance</span> /
    <span style="color:#4A9EDB;">support</span>).
    Edge thickness = co-occurrence intensity.
    Cross-cluster edges are intentionally faint.
</p>
""", unsafe_allow_html=True)

_net3 = go.Figure()

# Background cluster ellipses
_net3.add_shape(type="circle", x0=-1.12, y0=-0.72, x1=-0.28, y1=0.78,
                fillcolor="rgba(186,117,23,0.03)",
                line=dict(color="rgba(186,117,23,0.10)", width=1, dash="dot"), layer="below")
_net3.add_annotation(x=-0.70, y=0.84, text="Engineering & Materials",
                     font=dict(size=9, color="rgba(186,117,23,0.40)", family="Inter, sans-serif"),
                     showarrow=False)
_net3.add_shape(type="circle", x0=0.38, y0=-0.70, x1=1.12, y1=0.74,
                fillcolor="rgba(74,158,219,0.03)",
                line=dict(color="rgba(74,158,219,0.10)", width=1, dash="dot"), layer="below")
_net3.add_annotation(x=0.75, y=0.80, text="Ecology & Life Sciences",
                     font=dict(size=9, color="rgba(74,158,219,0.40)", family="Inter, sans-serif"),
                     showarrow=False)
_net3.add_annotation(x=0.0, y=0.0, text="← the gap →",
                     font=dict(size=9, color="rgba(200,196,188,0.18)", family="Inter, sans-serif"),
                     showarrow=False)

# Edge traces
for (_a, _b, _w) in _EDGES3:
    _x0, _y0 = _NODES3[_a][0], _NODES3[_a][1]
    _x1, _y1 = _NODES3[_b][0], _NODES3[_b][1]
    _is_cross = (_NODES3[_a][4] != _NODES3[_b][4])
    _op  = max(0.04, _w * 0.55) if not _is_cross else max(0.03, _w * 0.35)
    _wd  = max(0.5, _w * 3.5)   if not _is_cross else max(0.4, _w * 1.8)
    _net3.add_trace(go.Scatter(
        x=[_x0, _x1, None], y=[_y0, _y1, None], mode="lines",
        line=dict(width=_wd, color=f"rgba(200,196,188,{_op:.2f})"),
        hoverinfo="skip", showlegend=False,
    ))

# Node traces — one per paradigm for legend
# Improvement #1: only show text labels for large nodes (size >= 40)
# and use position-aware text placement to reduce overlap
_TEXT_POS = {
    "Materials Science":   "top center",
    "Mech. Engineering":   "bottom center",
    "Chemistry":           "bottom left",
    "Robotics":            "bottom center",
    "Biomedical Eng.":     "top center",
    "Nanotechnology":      "top left",
    "Environmental Sci.":  "top center",
    "Ecology":             "top right",
    "Biology":             "bottom center",
    "Conservation Bio.":   "bottom right",
    "Agriculture":         "top right",
    "Architecture/Design": "bottom center",
    "Computer Science":    "top center",
}

for _par3 in ["Replace", "Enhance", "Support"]:
    _nx, _ny, _nsz, _nlbl, _nhtxt, _ntpos = [], [], [], [], [], []
    for _nname, (_nx_, _ny_, _nsz_, _npar_, _ncl_, _npl_) in _NODES3.items():
        if _npar_ != _par3:
            continue
        _nx.append(_nx_); _ny.append(_ny_); _nsz.append(_nsz_)
        # Improvement: only label nodes with size >= 40
        _nlbl.append(_nname if _nsz_ >= 40 else "")
        _ntpos.append(_TEXT_POS.get(_nname, "top center"))
        _nhtxt.append(
            f"<b>{_nname}</b><br>Dominant paradigm: {_npar_}<br>"
            f"Cluster: {_ncl_}<br>{_npl_}"
        )
    _net3.add_trace(go.Scatter(
        x=_nx, y=_ny, mode="markers+text", name=_par3,
        text=_nlbl, textposition=_ntpos,
        textfont=dict(size=9, color="#5E626E", family="Inter, sans-serif"),
        hoverinfo="text", hovertext=_nhtxt,
        marker=dict(size=_nsz, color=_PAR_COLORS3[_par3],
                    line=dict(width=1.5, color=_PAR_BORDER3[_par3])),
    ))

_net3.update_layout(
    paper_bgcolor="#0A0E14", plot_bgcolor="#0E1320",
    height=520, margin=dict(l=20, r=20, t=20, b=20),
    showlegend=True,
    legend=dict(orientation="h", y=-0.04, x=0.5, xanchor="center",
                font=dict(size=11, color="#6A6E78", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    hovermode="closest",
    hoverlabel=dict(bgcolor="#0E1320", bordercolor="#1C2230",
                    font=dict(size=11, color="#C8C4BE", family="Inter, sans-serif")),
    xaxis=dict(visible=False, range=[-1.25, 1.25]),
    yaxis=dict(visible=False, range=[-0.90, 0.96]),
)
st.plotly_chart(_net3, use_container_width=True, config={"displayModeBar": False})

# ── Zone C: RoboBee case study (components.html) ──────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Case study — RoboBee</div>', unsafe_allow_html=True)
credibility_badge(has_real=False, has_sim=True)

components.html("""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; color: #E2DDD6; }
  .case-wrapper { background: #0E1320; border: 1px solid #1C2230; border-radius: 12px; padding: 1.6rem 1.8rem; }
  .case-header { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: #E2DDD6; margin-bottom: .25rem; }
  .case-meta { font-size: .7rem; font-weight: 300; color: #2A2E3A; margin-bottom: 1.4rem; letter-spacing: .08em; text-transform: uppercase; }
  .case-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 1.1rem; }
  .case-col { background: #0A0E14; border: 1px solid #1C2230; border-radius: 8px; padding: 1.1rem 1rem; }
  .case-col.col-eng  { border-top: 2px solid rgba(186,117,23,0.5); }
  .case-col.col-eco  { border-top: 2px solid rgba(74,158,219,0.5); }
  .case-col.col-both { border-top: 2px solid rgba(90,156,110,0.5); }
  .case-col-title { font-size: .7rem; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .75rem; }
  .col-eng  .case-col-title { color: rgba(186,117,23,0.85); }
  .col-eco  .case-col-title { color: rgba(74,158,219,0.85); }
  .col-both .case-col-title { color: rgba(90,156,110,0.85); }
  ul { padding-left: 1.1rem; list-style: disc; }
  ul li { font-size: .75rem; font-weight: 300; line-height: 1.7; color: #3A404F; margin-bottom: .15rem; }
  ul li b { color: #6A6E78; font-weight: 500; }
  ul li em { color: #5A9C6E; font-style: italic; }
  .case-footer { font-size: .78rem; font-weight: 300; font-style: italic; line-height: 1.65; color: #2A2E3A; border-top: 1px solid #161B26; padding-top: .9rem; }
</style></head><body>
<div class="case-wrapper">
  <div class="case-header">The Incomplete Invention</div>
  <div class="case-meta">Harvard Microrobotics Lab &middot; 2013 &ndash; present</div>
  <div class="case-grid">
    <div class="case-col col-eng">
      <div class="case-col-title">What engineering sees</div>
      <ul>
        <li><b>Achieved:</b> insect-scale flapping-wing flight</li>
        <li><b>Achieved:</b> autonomous crop pollination in lab conditions</li>
        <li><b>Achieved:</b> millimetre-scale actuator design</li>
        <li><b>Achieved:</b> swarm coordination protocols</li>
        <li><b>Status:</b> a landmark biomimetic success</li>
      </ul>
    </div>
    <div class="case-col col-eco">
      <div class="case-col-title">What ecology sees</div>
      <ul>
        <li><b>Missing:</b> food source for insectivores (birds, bats)</li>
        <li><b>Missing:</b> wax, propolis, and hive products</li>
        <li><b>Missing:</b> cultural and spiritual meaning of bees</li>
        <li><b>Missing:</b> soil aeration from burrowing behaviour</li>
        <li><b>Missing:</b> biodiversity indicator function</li>
      </ul>
    </div>
    <div class="case-col col-both">
      <div class="case-col-title">What dialogue could build</div>
      <ul>
        <li>A robot that tracks and reports on pollinator health</li>
        <li>Technology designed to <em>support</em> living bees, not replace them</li>
        <li>Sensors for early ecosystem stress detection</li>
        <li>Design briefs rooted in full ecological function, not single output</li>
        <li>Shared language between engineering and ecology</li>
      </ul>
    </div>
  </div>
  <div class="case-footer">
    &ldquo;RoboBees meet the engineering requirements to achieve the biological function of pollination,
    but not the complex functionality of a living bee that provides other services.&rdquo;
    &mdash; Jacobs et al. (2025)
  </div>
</div>
</body></html>
""", height=460)

# ── Zone D: Framing analysis diverging bar ────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Framing analysis · abstract vocabulary</div>',
            unsafe_allow_html=True)
st.markdown("""
<p class="chart-sub-label">
    Word frequency in the Replace-oriented subcorpus (left, amber)
    vs. the Support-oriented subcorpus (right, blue), per 1,000 abstracts.
    The disciplinary divide is not just structural — it is linguistic.
</p>
""", unsafe_allow_html=True)

_FRAMING3 = pd.DataFrame({
    "term": [
        "Stewardship", "Coexistence", "Symbiosis", "Holistic", "Resilience",
        "Restoration", "Partnership",
        "Synthetic", "Engineering", "Control",
        "Extraction", "Maximization", "Exploitation", "Optimization", "Substitution",
    ],
    "replace_freq": [-6, -9, -11, -14, -22, -7, -5, -68, -92, -115, -79, -102, -74, -86, -91],
    "support_freq": [44, 60, 68, 50, 78, 58, 40, 14, 20, 10, 7, 5, 4, 9, 6],
})

_frame3 = go.Figure()
_frame3.add_trace(go.Bar(
    y=_FRAMING3["term"], x=_FRAMING3["replace_freq"], orientation="h",
    name="Replace subcorpus (technological framing)",
    marker=dict(color="rgba(186,117,23,0.70)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Replace subcorpus: %{customdata:.0f} per 1,000 abstracts<extra></extra>",
    customdata=np.abs(_FRAMING3["replace_freq"]),
))
_frame3.add_trace(go.Bar(
    y=_FRAMING3["term"], x=_FRAMING3["support_freq"], orientation="h",
    name="Support subcorpus (ecological framing)",
    marker=dict(color="rgba(74,158,219,0.72)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Support subcorpus: %{x:.0f} per 1,000 abstracts<extra></extra>",
))
_frame3.add_vline(x=0, line_color="rgba(200,196,188,0.20)", line_width=1)
_frame3.add_annotation(x=-58, y=1.04, yref="paper", text="← Technological / Control",
    font=dict(size=9, color="rgba(186,117,23,0.45)", family="Inter, sans-serif"),
    showarrow=False, xanchor="right")
_frame3.add_annotation(x=58, y=1.04, yref="paper", text="Ecological / Relational →",
    font=dict(size=9, color="rgba(74,158,219,0.45)", family="Inter, sans-serif"),
    showarrow=False, xanchor="left")
_frame3.update_layout(
    barmode="relative", paper_bgcolor="#0A0E14", plot_bgcolor="#0E1320",
    height=520, margin=dict(l=10, r=20, t=30, b=55),
    hovermode="y unified",
    hoverlabel=dict(bgcolor="#0E1320", bordercolor="#1C2230",
                    font=dict(size=11, color="#C8C4BE", family="Inter, sans-serif")),
    legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                font=dict(size=11, color="#6A6E78", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    xaxis=dict(title=dict(text="Occurrences per 1,000 abstracts (simulated)",
                          font=dict(size=11, color="#3A404F")),
               tickfont=dict(size=11, color="#3A404F"),
               tickvals=[-120, -80, -40, 0, 40, 80],
               ticktext=["120", "80", "40", "0", "40", "80"],
               gridcolor="#141A26", linecolor="#1C2230", zeroline=False),
    yaxis=dict(tickfont=dict(size=11, color="#5E626E", family="Inter, sans-serif"),
               autorange="reversed", linecolor="#1C2230", gridcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(_frame3, use_container_width=True, config={"displayModeBar": False})

st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#20242E;margin-top:.4rem;padding-left:2px;">
    Discipline network is simulated from plausible WoS Categories co-occurrence patterns.
    Framing analysis word frequencies are simulated for illustration.
    RoboBee citation: Jafferis et al. (2019), <em>Nature</em> 570, 491–495.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#2A3840;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 4 · What 3% Teaches Us — Imagining a Different Possibility
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

section_sep()

st.markdown('<div class="s4-eyebrow">Section 04 · What 3% Teaches Us</div>', unsafe_allow_html=True)
st.markdown('<h2 class="s4-title">Imagining a Different Possibility.</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="s4-sub">
    Three percent is a small number. But it represents something important:
    proof that another way of doing bio-inspired design is possible —
    one that works <em>with</em> natural systems rather than replacing them.
</p>
<p class="s4-sub">
    What would happen if the research community redirected even a fraction
    of its attention? And when these technologies do exist, who can
    actually access them?
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone B: Sankey with scenario toggle ───────────────────────
_SCENARIOS4 = {
    "Current state  (Support = 3%)": {
        "replace": 580, "enhance": 390, "support": 30,
        "label_r": "Replace  58%", "label_e": "Enhance  39%", "label_s": "Support   3%",
        "callout": (
            "At <b>3%</b>, Support-oriented research sends only <b>~8 units</b> "
            "to Critical Services — the rarest, most foundational flows in the entire corpus."
        ),
    },
    "Scenario  (Support = 20%)": {
        "replace": 410, "enhance": 390, "support": 200,
        "label_r": "Replace  41%", "label_e": "Enhance  39%", "label_s": "Support  20%",
        "callout": (
            "At <b>20%</b>, the flow to Critical Services grows to <b>~70 units</b> — "
            "a <b>9× increase</b> — while Replace research still receives the majority."
        ),
    },
}

st.markdown('<div class="chart-label">A map of choices — where research attention flows</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)

st.markdown("""
<p class="chart-sub-label">
    The same total research effort, distributed differently.
    Toggle between the current state and a hypothetical scenario
    to see how the flow to Critical Services changes.
    The green link is the pathway that matters most.
</p>
""", unsafe_allow_html=True)

_scenario_key = st.radio(
    label="Select scenario",
    options=list(_SCENARIOS4.keys()),
    horizontal=True,
    label_visibility="collapsed",
)
_sc4 = _SCENARIOS4[_scenario_key]
st.markdown(f'<div class="scenario-callout">{_sc4["callout"]}</div>', unsafe_allow_html=True)
_sankey4 = build_sankey(
    _sc4["replace"], _sc4["enhance"], _sc4["support"],
    _sc4["label_r"], _sc4["label_e"], _sc4["label_s"],
)
st.plotly_chart(_sankey4, use_container_width=True, config={"displayModeBar": False})

# ── Zone C: Global accessibility map ─────────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Global reach — who can access replacement technologies?</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=False, has_sim=True)
st.markdown("""
<p class="chart-sub-label">
    Bubble size = volume of Replace-oriented bio-inspired publications.
    Colour = open-access rate (green = freely available; red = paywalled).
    The countries producing the most replacement technologies
    are also the ones most likely to lock them behind patents and paywalls.
</p>
""", unsafe_allow_html=True)

_MAP_DATA4 = pd.DataFrame({
    "Country": [
        "United States", "China", "Germany", "United Kingdom",
        "Canada", "Australia", "France", "Japan", "South Korea",
        "Brazil", "India", "South Africa", "Mexico", "Kenya", "Nigeria", "Indonesia",
    ],
    "Region": (["Global North"] * 9) + (["Global South"] * 7),
    "Replace_Papers": [5200, 4800, 2100, 1800, 1200, 850, 1550, 1320, 580,
                       350, 720, 160, 140, 32, 18, 95],
    "Open_Access_Pct": [28, 22, 68, 72, 48, 55, 62, 35, 40,
                        82, 34, 88, 78, 95, 92, 86],
})

_map4 = px.scatter_geo(
    _MAP_DATA4, locations="Country", locationmode="country names",
    size="Replace_Papers", color="Open_Access_Pct",
    hover_name="Country",
    hover_data={"Country": False, "Region": True,
                "Replace_Papers": True, "Open_Access_Pct": ":.0f"},
    color_continuous_scale=[
        [0.0, "#8B1A1A"], [0.35, "#C07040"], [0.65, "#3D6B4F"], [1.0, "#5A9C6E"],
    ],
    range_color=[15, 100],
    color_continuous_midpoint=50,   # Improvement #4: force midpoint at 50%
    size_max=48,
    labels={"Open_Access_Pct": "Open Access %"},
)
_map4.update_geos(
    showcountries=True, countrycolor="rgba(28,34,48,0.8)",
    showcoastlines=True, coastlinecolor="rgba(28,34,48,0.6)",
    showland=True, landcolor="#0E1320",
    showocean=True, oceancolor="#0A0E14",
    showframe=False, projection_type="natural earth",
)
_map4.update_layout(
    paper_bgcolor="#0A0E14", geo_bgcolor="#0A0E14",
    height=440, margin=dict(r=0, t=10, l=0, b=0),
    coloraxis_colorbar=dict(
        title=dict(text="Open Access %", font=dict(size=11, color="#3A404F")),
        tickfont=dict(size=10, color="#3A404F"), ticksuffix="%",
        thickness=12, len=0.6,
        bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
    ),
    hoverlabel=dict(bgcolor="#0E1320", bordercolor="#1C2230",
                    font=dict(size=11, color="#C8C4BE", family="Inter, sans-serif")),
)
st.plotly_chart(_map4, use_container_width=True, config={"displayModeBar": False})

# ── Zone D: 3% Spotlight cards ────────────────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">The 3% — four technologies that chose to support</div>',
            unsafe_allow_html=True)

components.html("""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
  .card { background: #0E1320; border: 1px solid #1C2230; border-radius: 10px; padding: 1.3rem 1.2rem 1.1rem; border-top: 2px solid rgba(90,156,110,0.45); }
  .card-top { display: flex; align-items: flex-start; gap: 10px; margin-bottom: .85rem; }
  .card-icon { font-size: 1.6rem; line-height: 1; flex-shrink: 0; margin-top: 2px; }
  .card-meta { flex: 1; }
  .card-title { font-family: 'Playfair Display', serif; font-size: .95rem; font-weight: 700; color: #C8C4BE; line-height: 1.25; margin-bottom: 3px; }
  .card-service { font-size: .62rem; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: rgba(90,156,110,0.75); }
  .card-body { font-size: .75rem; font-weight: 300; line-height: 1.72; color: #3A404F; margin-bottom: .85rem; }
  .card-body em { color: #5A9C6E; font-style: italic; }
  .card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: .7rem; border-top: 1px solid #161B26; }
  .card-n { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: #4A9EDB; }
  .card-n-label { font-size: .62rem; font-weight: 300; color: #2A2E3A; margin-top: 1px; }
  .card-paradigm { font-size: .62rem; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; padding: 3px 9px; border-radius: 20px; background: rgba(74,158,219,0.10); color: rgba(74,158,219,0.80); border: 1px solid rgba(74,158,219,0.18); }
</style></head><body>
<div class="grid">
  <div class="card">
    <div class="card-top">
      <div class="card-icon">🦪</div>
      <div class="card-meta">
        <div class="card-title">Living Shoreline Systems</div>
        <div class="card-service">Coastline Regulation · Supporting</div>
      </div>
    </div>
    <div class="card-body">Bio-inspired breakwater structures modelled on oyster reef geometry to dissipate wave energy while providing substrate for marine organisms. Unlike concrete seawalls, these structures <em>support</em> the colonisation and growth of natural reef communities over time — the technology becomes more effective as nature reclaims it.</div>
    <div class="card-footer">
      <div><div class="card-n">~15</div><div class="card-n-label">papers in corpus</div></div>
      <div class="card-paradigm">Support</div>
    </div>
  </div>
  <div class="card">
    <div class="card-top">
      <div class="card-icon">🍄</div>
      <div class="card-meta">
        <div class="card-title">Mycorrhizal Network Inoculants</div>
        <div class="card-service">Primary Production · Supporting</div>
      </div>
    </div>
    <div class="card-body">Fungal network-inspired soil amendments that enhance plant nutrient uptake by inoculating degraded soils with mycorrhizal consortia. Rather than replacing soil biology, this approach <em>reactivates</em> dormant underground networks — using the wood-wide web's own logic to restore carbon sequestration in post-industrial landscapes.</div>
    <div class="card-footer">
      <div><div class="card-n">~8</div><div class="card-n-label">papers in corpus</div></div>
      <div class="card-paradigm">Support</div>
    </div>
  </div>
  <div class="card">
    <div class="card-top">
      <div class="card-icon">🐝</div>
      <div class="card-meta">
        <div class="card-title">Pollinator Corridor Mapping</div>
        <div class="card-service">Pollination · Supporting</div>
      </div>
    </div>
    <div class="card-body">Landscape connectivity models derived from bee foraging algorithms to design habitat corridors that <em>support</em> existing pollinator populations across fragmented agricultural land. Unlike RoboBees, this technology asks not how to replace bees — but how to make the landscape legible to them again.</div>
    <div class="card-footer">
      <div><div class="card-n">~20</div><div class="card-n-label">papers in corpus</div></div>
      <div class="card-paradigm">Support</div>
    </div>
  </div>
  <div class="card">
    <div class="card-top">
      <div class="card-icon">🦫</div>
      <div class="card-meta">
        <div class="card-title">Beaver-Inspired Wetland Restoration</div>
        <div class="card-service">Water Regulation · Supporting</div>
      </div>
    </div>
    <div class="card-body">Low-cost structures modelled on beaver dam geometry to slow water flow, raise water tables, and restore hydrological function in degraded stream systems. Where beaver populations are locally extinct, these structures <em>hold space</em> for recolonisation — designed to become redundant once the living engineer returns.</div>
    <div class="card-footer">
      <div><div class="card-n">~12</div><div class="card-n-label">papers in corpus</div></div>
      <div class="card-paradigm">Support</div>
    </div>
  </div>
</div>
</body></html>
""", height=700)

st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#20242E;margin-top:1rem;padding-left:2px;">
    Sankey flow values proportional to published findings in Jacobs et al. (2025).
    Scenario values are illustrative. Global map data is simulated.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#2A3840;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────
#  SECTION 5 · You Belong Here
# ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════

section_sep()

st.markdown('<div class="eyebrow">Section 05 · You Belong Here</div>', unsafe_allow_html=True)

# ── Zone A: Quote + pivot ─────────────────────────────────────
st.markdown("""
<div class="quote-wrap">
    <span class="quote-mark">&ldquo;</span>
    <p class="quote-text">
        Some can be mimicked. Very few can be entirely replaced.
        None should be rendered optional.
    </p>
    <span class="quote-source">Jacobs et al. (2025) · Biomimetics 10, 784</span>
    <p class="turn-text">
        You have just seen twenty years of data.
        You have seen the gaps, the islands, the imbalances.
        <br><br>
        But this is not a story about what is missing.
        <em>It is a story about what is possible</em> —
        and about who gets to help build it.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone B: Data echo — callback from Section 0 ───────────────
# Read the user's Section 0 selections from session_state.
# Three adaptive states:
#   (a) user did not interact with Section 0  → show static fallback
#   (b) all selected services are well-researched → positive framing
#   (c) some / all selected services are in the gap → personalised impact
_all_svc_flat5 = [s for cat in SERVICES.values() for s in cat["items"]]
_selected5     = [s for s in _all_svc_flat5 if st.session_state.get(s["name"], False)]
_gap5          = [s for s in _selected5 if s["papers"] < RESEARCH_GAP_THRESHOLD]
_n_sel5        = len(_selected5)
_n_gap5        = len(_gap5)

if _n_sel5 == 0:
    _echo_n     = "15"
    _echo_body  = "of the 22 services nature provides have fewer than 500 bio-inspired research papers."
    _echo_sub   = ("That is not a research gap. That is an open invitation — "
                   "to every scientist, designer, policymaker, artist, and curious human reading this.")
elif _n_gap5 == 0:
    _echo_n     = str(_n_sel5)
    _echo_body  = (f"services you said you depend on today — and all are relatively well-studied. "
                   f"But most people's selections aren't.")
    _echo_sub   = "15 of the 22 services have fewer than 500 papers. The gap belongs to all of us."
else:
    _gap_names5 = ", ".join(f"<em>{s['name']}</em>" for s in _gap5[:3])
    _more5      = f" and {_n_gap5 - 3} more" if _n_gap5 > 3 else ""
    _echo_n     = str(_n_gap5)
    _echo_body  = (f"of the {_n_sel5} services you said you depend on today "
                   f"have fewer than 500 bio-inspired research papers — "
                   f"including {_gap_names5}{_more5}.")
    _echo_sub   = ("That gap is not abstract. It is the distance between what you need "
                   "and what science is currently building. And it has your name on it.")

st.markdown(f"""
<div class="echo-wrap">
    <span class="echo-n">{_echo_n}</span>
    <p class="echo-label">{_echo_body}</p>
    <p class="echo-sub">{_echo_sub}</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone C: Identity selector + personalised response ─────────
st.markdown('<div class="chart-label">Who are you in this story?</div>', unsafe_allow_html=True)
st.markdown("""
<p style="font:300 .82rem/1.6 'Inter',sans-serif;color:#2E3648;max-width:520px;margin-bottom:1rem;">
    Select the role that feels closest to you.
    We have something to say to each of you.
</p>
""", unsafe_allow_html=True)

_IDENTITIES5 = [
    ("🔬", "Researcher\n/ Scientist",  "researcher"),
    ("✏️", "Designer\n/ Engineer",     "designer"),
    ("📋", "Policymaker\n/ Funder",    "policymaker"),
    ("🎨", "Artist\n/ Writer",         "artist"),
    ("📚", "Educator\n/ Student",      "educator"),
    ("🌍", "Curious\nHuman",           "human"),
]
_cols5 = st.columns(6)
for _col5, (_icon5, _lbl5, _key5) in zip(_cols5, _IDENTITIES5):
    with _col5:
        if st.button(f"{_icon5}  {_lbl5}", key=f"id_{_key5}", use_container_width=True):
            st.session_state.identity = _key5

_RESPONSES5 = {
    "researcher": {
        "title": "The map has your name on it.",
        "body": (
            "Pollination: <b>355 papers.</b> Nutrient cycling: <b>58 papers.</b> "
            "Soil formation: <b>343 papers.</b><br><br>"
            "These are not obscure niches — they are the foundations of global food security. "
            "They are also among the least-funded, least-published areas in the entire "
            "bio-inspired corpus. That gap exists not because the questions are unanswerable, "
            "but because the incentive structures haven't pointed there yet.<br><br>"
            "<em>Your next paper, your next grant proposal, your next collaboration across "
            "a disciplinary boundary — that is how the map changes.</em>"
        ),
        "links": [
            ("Read the full paper", "https://doi.org/10.3390/biomimetics10110784"),
            ("Join the MEco seminar series", "https://www.manufacturedecosystems.com/seminar-series"),
            ("Explore the project", "https://www.manufacturedecosystems.com/projects"),
        ],
    },
    "designer": {
        "title": "Nature is the best brief you have never been given.",
        "body": (
            "The 3% of bio-inspired research that chooses to <em>support</em> living systems "
            "rather than replace them — that work needed designers too. "
            "It needed someone to ask: what does a water system that becomes redundant "
            "once nature recovers actually look like?<br><br>"
            "The dominant paradigm — Replace — produces things that can be patented and sold. "
            "The Support paradigm produces things that work best when they disappear. "
            "<em>That is a harder, more interesting design problem. "
            "And it is almost entirely unoccupied.</em>"
        ),
        "links": [
            ("See the virtual exhibition", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
            ("Call for artists", "https://www.manufacturedecosystems.com/art-apply"),
            ("Learning from nature", "https://www.manufacturedecosystems.com/home/learning-from-nature"),
        ],
    },
    "policymaker": {
        "title": "You hold the dial.",
        "body": (
            "The reason Critical Services — pollination, soil formation, nutrient cycling — "
            "have so few research papers is not that scientists don't care. "
            "It is that <b>funding flows toward what can be patented, commercialised, "
            "and sold.</b><br><br>"
            "A single grant program focused on Support-oriented, openly-licensed "
            "bio-inspired research could shift the entire distribution. "
            "<em>The lever is small. The effect is large. "
            "And the decision sits with people like you.</em>"
        ),
        "links": [
            ("Read the research", "https://doi.org/10.3390/biomimetics10110784"),
            ("About the MEco project", "https://www.manufacturedecosystems.com/about-us"),
            ("Get in touch", "https://www.manufacturedecosystems.com/contact"),
        ],
    },
    "artist": {
        "title": "Imagination shapes what science thinks is possible.",
        "body": (
            "The Manufactured Ecosystems project was built on a belief that "
            "this research team holds with conviction: <em>the stories we tell about "
            "nature — in fiction, in art, in poetry, in film — shape the futures "
            "that scientists and engineers think are worth building.</em><br><br>"
            "Your image, your sentence, your character who misses a river that no longer runs — "
            "that is not separate from the data you have just seen. "
            "<b>It is the data, felt from the inside.</b><br><br>"
            "The MEco Anthology is looking for writers. The Exhibition is looking for artists."
        ),
        "links": [
            ("Virtual Exhibition 2025", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
            ("Call for artists", "https://www.manufacturedecosystems.com/art-apply"),
            ("Learning from imagination", "https://www.manufacturedecosystems.com/home/learning-from-imagination"),
        ],
    },
    "educator": {
        "title": "The silos were built in classrooms. They can be taken down there too.",
        "body": (
            "The disciplinary isolation we showed you in Section 3 — "
            "engineers on one island, ecologists on the other — "
            "was not inevitable. It was constructed, over decades, "
            "through curricula that trained people to stay in their lanes.<br><br>"
            "A single course that asks an engineering student and an ecology student "
            "to design something together — with a shared vocabulary and no clean disciplinary exit — "
            "<em>that course is already changing the map.</em>"
        ),
        "links": [
            ("Seminar series", "https://www.manufacturedecosystems.com/seminar-series"),
            ("About the team", "https://www.manufacturedecosystems.com/about-us"),
            ("MEco projects", "https://www.manufacturedecosystems.com/projects"),
        ],
    },
    "human": {
        "title": "You have already done the most important thing.",
        "body": (
            "You came here. You read this. You thought about which ecosystem services "
            "you depend on before you had ever heard the phrase "
            "&ldquo;ecosystem service.&rdquo;<br><br>"
            "That attention — that willingness to sit with the complexity, "
            "the data, the gaps, the possibilities — "
            "<em>that is the rarest thing in the world right now.</em> "
            "Not expertise. Not funding. Not technology. Attention.<br><br>"
            "Share this with one person who would find it uncomfortable. "
            "Ask one question in a meeting that nobody has thought to ask. "
            "Visit the exhibition. Read the fiction. Come back.<br><br>"
            "<b>You belong in this conversation.</b> You always did."
        ),
        "links": [
            ("Explore MEco", "https://www.manufacturedecosystems.com"),
            ("Virtual Exhibition", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
            ("Learning from each other", "https://www.manufacturedecosystems.com/home/learning-from-each-other"),
        ],
    },
}

if st.session_state.identity and st.session_state.identity in _RESPONSES5:
    _resp5 = _RESPONSES5[st.session_state.identity]
    _links5 = "".join(
        f'<a class="r-btn" href="{_url}" target="_blank">{_lbl}</a>'
        for _lbl, _url in _resp5["links"]
    )
    st.markdown(f"""
    <div class="response-card">
        <div class="response-title">{_resp5["title"]}</div>
        <div class="response-body">{_resp5["body"]}</div>
        <div class="response-actions">{_links5}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="font:300 .8rem/1 'Inter',sans-serif;color:#1C2230;
              margin-top:.5rem;font-style:italic;">
        Select a role above to receive a personalised message.
    </p>
    """, unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Zone D: MEco pathway cards ────────────────────────────────
st.markdown('<div class="chart-label">Ways to engage with Manufactured Ecosystems</div>',
            unsafe_allow_html=True)

components.html("""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .card { background: #0E1320; border: 1px solid #1C2230; border-radius: 10px; padding: 1.3rem 1.2rem; text-decoration: none; display: block; transition: border-color .22s, background .22s; }
  .card:hover { border-color: rgba(90,156,110,0.38); background: rgba(74,124,89,0.05); }
  .card-icon { font-size: 1.4rem; display: block; margin-bottom: .6rem; }
  .card-title { font-family: 'Playfair Display', serif; font-size: .92rem; font-weight: 700; color: #C8C4BE; margin-bottom: .4rem; line-height: 1.25; }
  .card-desc { font-size: .72rem; font-weight: 300; color: #2A2E3A; line-height: 1.6; margin-bottom: .9rem; }
  .card-cta { font-size: .62rem; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: rgba(90,156,110,0.60); }
</style></head><body>
<div class="grid">
  <a class="card" href="https://www.manufacturedecosystems.com/virtual-exhibition-2025" target="_blank">
    <span class="card-icon">🌿</span>
    <div class="card-title">Virtual Exhibition 2025</div>
    <div class="card-desc">Explore the live exhibition — art, VR, and community reflections on what a technology-realised wetland might look like. Available now, from anywhere in the world.</div>
    <div class="card-cta">Explore the exhibition →</div>
  </a>
  <a class="card" href="https://www.manufacturedecosystems.com/seminar-series" target="_blank">
    <span class="card-icon">🎙️</span>
    <div class="card-title">Seminar Series</div>
    <div class="card-desc">Transdisciplinary conversations at the edge of biology, engineering, design, and the humanities. Open to researchers, practitioners, and curious minds at every stage.</div>
    <div class="card-cta">View upcoming seminars →</div>
  </a>
  <a class="card" href="https://doi.org/10.3390/biomimetics10110784" target="_blank">
    <span class="card-icon">📄</span>
    <div class="card-title">The Research Paper</div>
    <div class="card-desc">The peer-reviewed study behind this dashboard. Jacobs et al. (2025), <em>Biomimetics</em> 10, 784. Open access — free for anyone, anywhere.</div>
    <div class="card-cta">Read the paper →</div>
  </a>
  <a class="card" href="https://www.manufacturedecosystems.com/home/learning-from-nature" target="_blank">
    <span class="card-icon">🌱</span>
    <div class="card-title">Learning from Nature</div>
    <div class="card-desc">Dive deeper into the four knowledge pillars of the project — Nature, Technology, Imagination, and Each Other. A growing library of resources for all disciplines.</div>
    <div class="card-cta">Start exploring →</div>
  </a>
  <a class="card" href="https://www.manufacturedecosystems.com/about-us" target="_blank">
    <span class="card-icon">🤝</span>
    <div class="card-title">The Team</div>
    <div class="card-desc">An international, cross-disciplinary collective of biologists, engineers, designers, literary scholars, artists, and educators working toward a shared question.</div>
    <div class="card-cta">Meet the team →</div>
  </a>
  <a class="card" href="https://www.manufacturedecosystems.com/contact" target="_blank">
    <span class="card-icon">✉️</span>
    <div class="card-title">Get in Touch</div>
    <div class="card-desc">Have a collaboration idea? A research question? A story to tell? The Manufactured Ecosystems project is actively looking for new partners, contributors, and conversations.</div>
    <div class="card-cta">Start a conversation →</div>
  </a>
</div>
</body></html>
""", height=450)

# ── Zone E: Final statement ───────────────────────────────────
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="final-wrap">
    <span class="final-you">You</span>
    <span class="final-belong">Belong Here.</span>
    <a class="final-link" href="https://www.manufacturedecosystems.com" target="_blank">
        manufacturedecosystems.com
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p class="land-ack">
    The Dish with One Spoon Covenant speaks to our collective responsibility
    to steward and sustain the land and environment in which we live and work,
    so that all peoples, present and future, may benefit from the sustenance it provides.
    We recognise the partnerships and knowledge that have guided the learning
    and research conducted as part of this work.
</p>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
