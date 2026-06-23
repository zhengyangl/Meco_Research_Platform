"""
MEco Research Dashboard — Complete Single-Page Application (v3)
"Nature Is Not Optional."
Based on Jacobs et al. (2025), Biomimetics 2025, 10, 784
"""

# ════════════════════════════════════════════════════════════════
# IMPORTS
# ════════════════════════════════════════════════════════════════
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import json

# ════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Nature Is Not Optional · MEco",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════
# GLOBAL CSS  (light theme)
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ─────────────────────────────────────────────────── */
.stApp { background: #F7F5F1; color: #2A2722; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }
section.main > div { padding-top: 2.5rem; padding-bottom: 6rem; }
div.block-container { max-width: 1080px; padding-left: 2rem; padding-right: 2rem; }

/* ── Shared utilities ─────────────────────────────────────── */
.hr     { border: none; border-top: 1px solid #E5E1DA; margin: 1.5rem 0; }
.hr-sm  { border: none; border-top: 1px solid #E5E1DA; margin: 1.2rem 0; }
.section-sep { border: none; border-top: 1px solid #DAD5CC; margin: 5rem 0 4rem; }
.chart-label {
    font: 500 0.68rem/1 'Inter', sans-serif;
    letter-spacing: .18em; text-transform: uppercase;
    color: #8A847B; margin-bottom: .6rem;
}
.chart-sub-label {
    font: 300 .82rem/1.6 'Inter', sans-serif;
    color: #6B665E; max-width: 600px; margin-bottom: .9rem;
}

/* ── Section eyebrows ─────────────────────────────────────── */
.hero-eyebrow, .s1-eyebrow, .s2-eyebrow,
.s3-eyebrow, .s4-eyebrow, .s6-eyebrow, .eyebrow {
    font: 500 0.68rem/1 'Inter', sans-serif;
    letter-spacing: .22em; text-transform: uppercase;
    color: #3D7A52; margin-bottom: .85rem;
}

/* ── Section 0: Hero ──────────────────────────────────────── */
.hero-eyebrow { font-size: 0.7rem; margin-bottom: .9rem; }
.hero-title {
    font: 700 3.8rem/1.05 'Playfair Display', serif;
    color: #2A2722; margin-bottom: .9rem;
}
.hero-sub {
    font: 300 1.08rem/1.8 'Inter', sans-serif;
    color: #6B665E; max-width: 540px; margin-bottom: 1.8rem;
}
.hero-prompt {
    font: 400 1rem/1.7 'Inter', sans-serif;
    color: #4A453E; padding: 1.1rem 1.5rem;
    border-left: 3px solid #3D7A52;
    border-radius: 0 8px 8px 0;
    background: rgba(61,122,82,.07);
}
.hero-prompt strong { color: #2A2722; font-weight: 500; }

/* ── Section 0: Category pills ───────────────────────────── */
.cat-pill {
    display: inline-block;
    font: 500 0.67rem/1 'Inter', sans-serif;
    letter-spacing: .16em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px;
    margin: 1.4rem 0 .7rem;
}
.cp-provisioning { background: rgba(168,116,14,.12); color: #8A5E0B; }
.cp-cultural      { background: rgba(95,87,189,.12);  color: #5048A8; }
.cp-regulating    { background: rgba(29,140,105,.12); color: #1A7A5C; }
.cp-supporting    { background: rgba(61,122,82,.12);  color: #356B49; }

/* ── Section 0: Counter ──────────────────────────────────── */
.ctr {
    text-align: center; background: #FBF9F5;
    border: 1px solid #E5E1DA; border-radius: 10px;
    padding: 1.6rem 2rem; margin: 1.2rem 0 1rem;
}
.ctr-n   { font: 700 3.2rem/1 'Playfair Display', serif; color: #3D7A52; }
.ctr-sub { font: 300 .82rem/1 'Inter', sans-serif; color: #8A847B; margin-top: 6px; }

/* ── Section 0: Insight panel ────────────────────────────── */
.insight {
    background: linear-gradient(145deg, #EEF4EE 0%, #F7F5F1 70%);
    border: 1px solid #C5DBCB; border-radius: 12px;
    padding: 2rem 2.4rem; margin-top: 1rem;
}
.insight-title { font: 700 1.55rem/1.25 'Playfair Display', serif; color: #2A2722; margin-bottom: .9rem; }
.insight-body  { font: 400 .96rem/1.85 'Inter', sans-serif; color: #4A453E; margin-bottom: 1.3rem; }
.hl-red   { font: 700 1.7rem/1 'Playfair Display', serif; color: #B05A2E; }
.hl-green { font: 700 1.7rem/1 'Playfair Display', serif; color: #3D7A52; }
.tag-sec-lbl { font: 500 .64rem/1 'Inter', sans-serif; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 5px; }
.lbl-gap { color: #B05A2E; }
.lbl-ok  { color: #3D7A52; }
.tag { display: inline-block; margin: 3px 3px; padding: 3px 9px; border-radius: 20px; font: 400 .7rem/1 'Inter', sans-serif; }
.tag-gap { background: rgba(176,90,46,.10); color: #97491F; border: 1px solid rgba(176,90,46,.25); }
.tag-ok  { background: rgba(61,122,82,.10); color: #356B49; border: 1px solid rgba(61,122,82,.25); }
.insight-cta   { font: 500 .75rem/1 'Inter', sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #3D7A52; }
.insight-empty { text-align: center; padding: 2rem; color: #B8B0A4; font: 300 .88rem/1.6 'Inter', sans-serif; }

div:has(> button[data-testid*="stBaseButton-pill"]) {
    justify-content: center !important;
    gap: 14px 12px !important;
    padding: 10px 0 20px 0;
}

button[data-testid="stBaseButton-pills"],
button[data-testid="stBaseButton-pillsActive"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E5E1DA !important;
    border-radius: 30px !important;
    padding: 10px 28px !important; 
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important; 
    letter-spacing: 0.02em !important; 
    color: #6B665E !important;
    box-shadow: 0 2px 4px rgba(42,39,34,0.02) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    height: auto !important; 
    min-height: 62px !important; 
}

button[data-testid="stBaseButton-pills"]:hover,
button[data-testid="stBaseButton-pillsActive"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 12px rgba(61,122,82,0.08) !important;
    border-color: rgba(61,122,82,0.3) !important;
    color: #2A2722 !important;
}

button[data-testid="stBaseButton-pills"]:active,
button[data-testid="stBaseButton-pillsActive"]:active {
    transform: translateY(1px) !important;
    box-shadow: 0 1px 2px rgba(61,122,82,0.1) !important;
}

button[data-testid="stBaseButton-pillsActive"] {
    background-color: rgba(61, 122, 82, 0.08) !important;
    border: 1.5px solid #3D7A52 !important;
    color: #356B49 !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 10px rgba(61, 122, 82, 0.1) !important;
    transform: translateY(0) !important; 
}

button[data-testid*="stBaseButton-pill"]:focus-visible {
    box-shadow: none !important;
    outline: none !important;
}

/* ── Section 1: Narrative ────────────────────────────────── */
.s1-title  { font: 700 3.4rem/1.08 'Playfair Display', serif; color: #2A2722; margin-bottom: .85rem; }
.s1-sub    { font: 300 1.05rem/1.85 'Inter', sans-serif; color: #6B665E; max-width: 580px; margin-bottom: .5rem; }
.s1-bridge {
    font: 400 1.0rem/1.7 'Inter', sans-serif; color: #4A453E;
    padding: 1rem 1.5rem; border-left: 3px solid #3D7A52;
    border-radius: 0 8px 8px 0; background: rgba(61,122,82,.07);
    margin-bottom: 1.6rem;
}
.s1-bridge em { color: #2A2722; font-style: normal; font-weight: 500; }

/* ── Section 1: KPI cards ────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.4rem; }
.kpi-card { background: #FFFFFF; border: 1px solid #E5E1DA; border-radius: 10px; padding: 1.2rem 1.1rem 1rem; text-align: center; box-shadow: 0 1px 2px rgba(42,39,34,.03); }
.kpi-card.accent-amber { border-color: #E0C589; }
.kpi-card.accent-green { border-color: #B6D2BD; }
.kpi-val       { font: 700 2.1rem/1 'Playfair Display', serif; color: #2A2722; display: block; margin-bottom: .45rem; }
.kpi-val-amber { color: #A8740E !important; }
.kpi-val-green { color: #3D7A52 !important; }
.kpi-label     { font: 500 .75rem/1.3 'Inter', sans-serif; color: #6B665E; display: block; margin-bottom: .3rem; }
.kpi-note      { font: 300 .67rem/1.45 'Inter', sans-serif; color: #9A938A; display: block; }

/* ── Section 2 / 3 / 4 / 6 narrative ─────────────────────── */
.s2-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #2A2722; margin-bottom: .85rem; }
.s2-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #6B665E; max-width: 600px; margin-bottom: .5rem; }
.s3-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #2A2722; margin-bottom: .85rem; }
.s3-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #6B665E; max-width: 600px; margin-bottom: .5rem; }
.s4-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #2A2722; margin-bottom: .85rem; }
.s4-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #6B665E; max-width: 600px; margin-bottom: .5rem; }
.s6-title { font: 700 3.2rem/1.08 'Playfair Display', serif; color: #2A2722; margin-bottom: .85rem; }
.s6-sub   { font: 300 1.02rem/1.85 'Inter', sans-serif; color: #6B665E; max-width: 620px; margin-bottom: .5rem; }
div[data-testid="stRadio"] label { font: 400 .82rem/1 'Inter', sans-serif !important; color: #4A453E !important; }
div[data-testid="stRadio"] > div { gap: 1rem; }
.scenario-callout {
    background: rgba(61,122,82,0.07); border: 1px solid rgba(61,122,82,0.22);
    border-left: 3px solid #3D7A52; border-radius: 0 8px 8px 0;
    padding: .85rem 1.2rem; font: 300 .82rem/1.65 'Inter', sans-serif;
    color: #4A453E; margin-bottom: 1rem;
}
/* ── Section 2: Radial chart side panel ──────────────────── */
.radial-info-card {
    background: #FBF9F5; border: 1px solid #E5E1DA; border-radius: 10px;
    padding: 1.1rem 1.3rem; margin-bottom: 1rem;
}
.radial-info-card.insight {
    background: linear-gradient(145deg, #EEF4EE 0%, #FBF9F5 75%);
    border-color: #C5DBCB;
}
.radial-info-title {
    font: 600 .66rem/1 'Inter', sans-serif; letter-spacing: .16em; text-transform: uppercase;
    color: #9A938A; margin-bottom: .7rem;
}
.radial-info-card.insight .radial-info-title { color: #3D7A52; }
.radial-info-body { font: 300 .82rem/1.7 'Inter', sans-serif; color: #6B665E; }
.radial-info-body b { color: #2A2722; font-weight: 500; }
.radial-info-body .ib-su { color: #2E7CB8; font-weight: 500; }
.radial-info-body .ib-en { color: #1D8C69; font-weight: 500; }
.radial-info-body .ib-re { color: #A8740E; font-weight: 500; }

.scenario-callout b { color: #356B49; font-weight: 500; }



/* ── Section 2: Gap cards ────────────────────────────────── */
.gap-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 1.4rem 0; }
.gap-card { background: #FFFFFF; border: 1px solid #E5E1DA; border-radius: 10px; padding: 1.3rem 1.2rem 1.1rem; box-shadow: 0 1px 2px rgba(42,39,34,.03); }
.gap-card.critical { border-color: #E0B79E; }
.gap-icon  { font-size: 1.5rem; display: block; margin-bottom: .55rem; }
.gap-svc   { font: 500 .82rem/1.2 'Inter', sans-serif; color: #4A453E; letter-spacing: .06em; margin-bottom: .55rem; }
.gap-n     { font: 700 2.3rem/1 'Playfair Display', serif; color: #B05A2E; display: block; margin-bottom: .4rem; }
.gap-n-ok  { color: #3D7A52 !important; }
.gap-sub   { font: 300 .72rem/1.5 'Inter', sans-serif; color: #8A847B; }
.gap-ratio { font: 300 .68rem/1 'Inter', sans-serif; color: #6B665E; margin-top: .7rem; padding-top: .7rem; border-top: 1px solid #E5E1DA; }
.gap-ratio b { color: #B05A2E; }

/* ── Section 5: Quote ────────────────────────────────────── */
.quote-wrap { text-align: center !important; padding: 3.5rem 2rem 2rem !important; max-width: 720px !important; margin: 0 auto !important; }
.quote-mark { font: 400 4rem/1 'Playfair Display', serif !important; color: rgba(61,122,82,0.30) !important; display: block !important; margin-bottom: -.5rem !important; }
.quote-text { font: 400 italic 1.8rem/1.55 'Playfair Display', serif !important; color: #2A2722 !important; margin-bottom: 1.2rem !important; }
.quote-source { font: 300 .75rem/1 'Inter', sans-serif !important; color: #8A847B !important; letter-spacing: .10em !important; text-transform: uppercase !important; }
.turn-text { font: 300 1.05rem/1.85 'Inter', sans-serif !important; color: #4A453E !important; text-align: center !important; max-width: 520px !important; margin: 2rem auto 0 !important; }
.turn-text em { color: #3D7A52 !important; font-style: normal !important; }

/* ── Section 5: Echo ─────────────────────────────────────── */
.echo-wrap {
    background: rgba(61,122,82,0.05) !important; border: 1px solid rgba(61,122,82,0.20) !important;
    border-radius: 14px !important; padding: 2.2rem 2.8rem !important;
    text-align: center !important; margin: 0 auto !important; max-width: 680px !important;
}
.echo-n     { font: 700 5rem/1 'Playfair Display', serif !important; color: #3D7A52 !important; display: block !important; margin-bottom: .6rem !important; }
.echo-label { font: 300 1.0rem/1.7 'Inter', sans-serif !important; color: #4A453E !important; max-width: 440px !important; margin: 0 auto .8rem !important; }
.echo-sub   { font: 300 .75rem/1.6 'Inter', sans-serif !important; color: #8A847B !important; max-width: 400px !important; margin: 0 auto !important; }

/* ── Section 5: Identity buttons ─────────────────────────── */
div[data-testid="stButton"] button {
    background: #FFFFFF !important; border: 1px solid #E5E1DA !important;
    border-radius: 10px !important; color: #4A453E !important;
    font: 400 .78rem/1.3 'Inter', sans-serif !important;
    height: 72px !important;
    box-shadow: 0 1px 2px rgba(42,39,34,.03) !important;
    transition: border-color .2s, background .2s !important;
}
div[data-testid="stButton"] button:hover {
    border-color: rgba(61,122,82,0.50) !important;
    background: rgba(61,122,82,0.05) !important; color: #2A2722 !important;
}
div[data-testid="stButton"] button:focus,
div[data-testid="stButton"] button:active {
    border-color: rgba(61,122,82,0.80) !important;
    background: rgba(61,122,82,0.09) !important; color: #2A2722 !important;
}

/* ── Section 5: Response card ────────────────────────────── */
.response-card {
    background: #FFFFFF !important; border: 1px solid #E5E1DA !important;
    border-left: 3px solid #3D7A52 !important; border-radius: 0 12px 12px 0 !important;
    padding: 2rem 2.4rem !important; margin-top: 1.4rem !important; max-width: 780px !important;
    box-shadow: 0 2px 6px rgba(42,39,34,.05) !important;
}
.response-title { font: 700 1.55rem/1.2 'Playfair Display', serif !important; color: #2A2722 !important; margin-bottom: .7rem !important; }
.response-body  { font: 300 .92rem/1.85 'Inter', sans-serif !important; color: #4A453E !important; margin-bottom: 1.2rem !important; }
.response-body em { color: #2E7CB8 !important; font-style: italic !important; }
.response-body b  { color: #2A2722 !important; font-weight: 500 !important; }
.response-actions { display: flex !important; flex-wrap: wrap !important; gap: 8px !important; }
.r-btn {
    font: 400 .72rem/1 'Inter', sans-serif !important; letter-spacing: .10em !important; text-transform: uppercase !important;
    padding: 7px 16px !important; border-radius: 20px !important;
    border: 1px solid rgba(61,122,82,0.40) !important; color: #356B49 !important;
    background: rgba(61,122,82,0.07) !important; text-decoration: none !important; display: inline-block !important;
}

/* ── Section 5: Final statement ──────────────────────────── */
.final-wrap { text-align: center !important; padding: 4rem 2rem 2rem !important; }
.final-you     { font: 300 1.1rem/1 'Inter', sans-serif !important; letter-spacing: .28em !important; text-transform: uppercase !important; color: #8A847B !important; margin-bottom: .6rem !important; display: block !important; }
.final-belong  { font: 700 4.2rem/1.1 'Playfair Display', serif !important; color: #3D7A52 !important; display: block !important; margin-bottom: 1.6rem !important; }
.final-link    { font: 400 .72rem/1 'Inter', sans-serif !important; letter-spacing: .18em !important; text-transform: uppercase !important; color: #356B49 !important; text-decoration: none !important; border-bottom: 1px solid rgba(61,122,82,0.35) !important; padding-bottom: 2px !important; display: inline-block !important; }
.land-ack      { font: 300 italic .75rem/1.8 'Inter', sans-serif !important; color: #B8B0A4 !important; max-width: 560px !important; display: block !important; margin: 3rem auto 0 !important; text-align: center !important; line-height: 1.85 !important; }

/* ── Credibility badges ───────────────────────────────────── */
.badge-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: .65rem; align-items: center; }
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    font: 400 .62rem/1 'Inter', sans-serif;
    letter-spacing: .10em; text-transform: uppercase;
    padding: 4px 10px; border-radius: 20px;
}
.badge-real { background: rgba(61,122,82,0.10); border: 1px solid rgba(61,122,82,0.30); color: #356B49; }
.badge-sim  { background: rgba(168,116,14,0.10); border: 1px solid rgba(168,116,14,0.28); color: #8A5E0B; }
.badge-dot  { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.badge-real .badge-dot { background: #3D7A52; }
.badge-sim  .badge-dot { background: #A8740E; }

/* ── Section 6: Data Sandbox tool styling ────────────────── */
.sandbox-note {
    background: #FBF9F5; border: 1px solid #E5E1DA; border-radius: 8px;
    padding: .8rem 1.2rem; font: 300 .74rem/1.6 'Inter', sans-serif;
    color: #8A847B; margin: .6rem 0 1.2rem;
}
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label {
    font: 500 .72rem/1.3 'Inter', sans-serif !important;
    color: #4A453E !important;
}
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
# DATA LOADING — read pre-computed JSON/Parquet from dashboard_data/
# ════════════════════════════════════════════════════════════════
# These files are produced by pipeline/aggregate.py on every pipeline run.
# The narrative page never queries the database directly — it reads only
# these static artifacts. This is what keeps the page loading instantly
# and what lets it survive even if the database is offline.
import json as _json
from pathlib import Path as _Path
_DATA_DIR = _Path(__file__).parent / "dashboard_data"

@st.cache_data
def _load_corpus_meta():
    with open(_DATA_DIR / "corpus_meta.json", encoding="utf-8") as f:
        return _json.load(f)

@st.cache_data
def _load_services_summary():
    with open(_DATA_DIR / "services_summary.json", encoding="utf-8") as f:
        return _json.load(f)

CORPUS = _load_corpus_meta()       # corpus_meta.json contents
SVC_SUMMARY = _load_services_summary()  # services_summary.json contents

# ── Service display-name mapping ────────────────────────────────────
# Database / aggregate.py stores the raw GPT classification values
# (e.g. 'Fibre/Hide/Wood', 'Atmospheric Regulation') as the source of truth.
# This dict turns those into the prettier display labels used throughout
# the narrative page. Anything not in this dict falls through to the raw
# value, so it's safe to leave the lookup unconditional.
SERVICE_DISPLAY_NAMES = {
    "Fibre/Hide/Wood":         "Fibre · Hide · Wood",
    "Atmospheric Regulation":  "Atmospheric Reg.",
    "Inspiration/Education":   "Inspiration · Education",
}
def display_name(raw: str) -> str:
    return SERVICE_DISPLAY_NAMES.get(raw, raw)


# ════════════════════════════════════════════════════════════════
# SHARED CONSTANTS
# ════════════════════════════════════════════════════════════════
RESEARCH_GAP_THRESHOLD = 500  # papers; services below this are flagged

# Service icon + description — these stay as code constants because they're
# editorial decisions (which emoji, how to describe each service) rather
# than data. Paper counts now come from JSON.
_SERVICE_META = {
    "Biochemicals":            {"icon": "🧬", "desc": "Molecules used in medicine"},
    "Fibre/Hide/Wood":         {"icon": "🌲", "desc": "Materials used for clothing or construction"},
    "Fuel":                    {"icon": "⚡", "desc": "Materials used to generate energy"},
    "Potable Water":           {"icon": "💧", "desc": "Fresh water that is safe to consume"},
    "Food":                    {"icon": "🌾", "desc": "Nutritious ingredients from wild & domesticated habitats"},
    "Biodiversity":            {"icon": "🦋", "desc": "The variety of living species on Earth"},
    "Disease Regulation":      {"icon": "🦠", "desc": "Natural systems reducing disease and disease vectors"},
    "Waste Treatment":         {"icon": "♻️", "desc": "Filtering and treating organic and chemical waste"},
    "Climate Regulation":      {"icon": "🌡️", "desc": "Stabilization of climatic conditions"},
    "Atmospheric Regulation":  {"icon": "💨", "desc": "Production and consumption of essential molecules (O₂)"},
    "Water Regulation":        {"icon": "🌊", "desc": "Timing and volume of water distribution across land"},
    "Pollination":             {"icon": "🐝", "desc": "Distribution of pollen seeds for plant reproduction"},
    "Coastline Regulation":    {"icon": "🏖️", "desc": "Stabilization of coastal lands via mangroves and reefs"},
    "Primary Production":      {"icon": "☀️", "desc": "Creation of sugars from sunlight — base of all food chains"},
    "Soil Formation":          {"icon": "🌱", "desc": "The ongoing creation of new fertile soil"},
    "Nutrient Cycling":        {"icon": "🔄", "desc": "The movement of nutrients through ecosystems"},
    "Inspiration/Education":   {"icon": "🎨", "desc": "Art, science, music, literature, and design"},
    "Aesthetic":               {"icon": "🌸", "desc": "Mental and physical benefits of natural beauty"},
    "Recreation":              {"icon": "🏕️", "desc": "Physical and mental health from nature experiences"},
    "Cultural Heritage":       {"icon": "🏛️", "desc": "Societal value placed upon landscapes"},
    "Spiritual":               {"icon": "🕊️", "desc": "Support for the spiritual lives of people"},
    "Cultural Identity":       {"icon": "🌍", "desc": "Individual and societal identity from human-nature bonds"},
}

# Build the same nested-dict structure the rest of the code expects, but now
# every paper count comes from services_summary.json — no hardcoded values.
_CAT_CSS_MAP = {"Provisioning": "provisioning", "Cultural": "cultural",
                "Regulating": "regulating", "Supporting": "supporting"}
SERVICES = {cat: {"css": _CAT_CSS_MAP[cat], "items": []} for cat in _CAT_CSS_MAP}
for _s in SVC_SUMMARY["services"]:
    _raw = _s["service"]
    _meta = _SERVICE_META.get(_raw, {"icon": "•", "desc": ""})
    SERVICES[_s["category"]]["items"].append({
        "name":   display_name(_raw),   # pretty label used everywhere downstream
        "icon":   _meta["icon"],
        "desc":   _meta["desc"],
        "papers": _s["total"],
    })

# Build _df2 directly from services_summary.json — single source of truth.
# The display_name() pass keeps the pretty service labels everywhere in the
# narrative; raw GPT names stay in the database and the data files.
_df2 = pd.DataFrame([
    {"service":  display_name(s["service"]),
     "category": s["category"],
     "total":    s["total"],
     "replace":  s["replace"],
     "enhance":  s["enhance"],
     "support":  s["support"]}
    for s in SVC_SUMMARY["services"]
])
_df2["adj"] = _df2["total"].clip(lower=1)

# ════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════
_svc_names = [s["name"] for cat in SERVICES.values() for s in cat["items"]]
for _name in _svc_names:
    if _name not in st.session_state:
        st.session_state[_name] = False

if "identity" not in st.session_state:
    st.session_state.identity = None

if "spotlight_idx" not in st.session_state:   # Section 4 carousel position
    st.session_state.spotlight_idx = 0


# ════════════════════════════════════════════════════════════════
# ONE-TIME OPENING ANIMATION 
# ════════════════════════════════════════════════════════════════
if not st.session_state.get("intro_played", False):
    st.session_state.intro_played = True
    
    components.html("""
    <script>
    (function() {
      try {
        var doc = window.parent.document;
        if (!doc.getElementById('meco-intro-style')) {
            var style = doc.createElement('style');
            style.id = 'meco-intro-style';
            style.innerHTML = `
              @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
              
              .meco-intro { position: fixed; inset: 0; z-index: 999999; background: #F7F5F1; overflow: hidden; cursor: pointer; display: flex; align-items: center; justify-content: center; opacity: 1; transition: opacity .85s ease; }
              .meco-intro.fade { opacity: 0; pointer-events: none; }
              .meco-intro canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
              
              .meco-intro .intro-center { position: relative; z-index: 2; text-align: center; padding: 0 1.5rem; opacity: 0; transform: translateY(10px); transition: opacity 1s ease .25s, transform 1s ease .25s; }
              .meco-intro.in .intro-center { opacity: 1; transform: translateY(0); }
              
              .meco-intro .intro-n { 
                  font: 700 4.2rem/1.05 'Playfair Display', serif; color: #2A2722; 
                  animation: meco-pulse-slow 6s infinite ease-in-out;
              }
              .meco-intro .intro-cap { font: 300 1.15rem/1.6 'Inter', sans-serif; color: #6B665E; margin-top: .7rem; }
              
              .meco-intro .intro-legend { margin-top: 1.8rem; display: flex; justify-content: center; gap: 24px; font: 400 .85rem/1 'Inter', sans-serif; color: #6B665E; }
              .meco-intro .leg-item { display: flex; align-items: center; gap: 8px; }
              .meco-intro .leg-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
              
              .meco-intro .intro-skip {
                  position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); z-index: 2;
                  font: 400 .75rem/1 'Inter', sans-serif; letter-spacing: .2em; text-transform: uppercase; color: #6B665E;
                  animation: meco-pulse 4.5s infinite ease-in-out;
              }
              
              @keyframes meco-pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
              @keyframes meco-pulse-slow { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }
              
              @media (max-width: 640px) { .meco-intro .intro-n { font-size: 2.6rem; } .meco-intro .intro-legend { flex-direction: column; gap: 12px; align-items: center; } }
            `;
            doc.head.appendChild(style);
        }

        if (doc.getElementById('meco-intro-singleton')) return;
        var ov = doc.createElement('div');
        ov.id = 'meco-intro-singleton';
        ov.className = 'meco-intro';
        
        ov.innerHTML =
          '<canvas></canvas>' +
          '<div class="intro-center">' +
            '<div class="intro-n">Nature Is Not Optional.</div>' +
            '<div class="intro-cap">Twenty years of bio-inspired research.<br>Each one a choice about nature.</div>' +
            '<div class="intro-legend">' +
              '<span class="leg-item"><span class="leg-dot" style="background:#A8740E;"></span> 58% Replace</span>' +
              '<span class="leg-item"><span class="leg-dot" style="background:#1D8C69;"></span> 39% Enhance</span>' +
              '<span class="leg-item"><span class="leg-dot" style="background:#2E7CB8;"></span> 3% Support</span>' +
            '</div>' +
          '</div>' +
          '<div class="intro-skip">Click anywhere to enter</div>';
          
        doc.body.appendChild(ov);
        requestAnimationFrame(function() { ov.classList.add('in'); });

        var canvas = ov.querySelector('canvas');
        var ctx = canvas.getContext('2d');
        var w, h;
        
        function resize() { 
            w = canvas.width = ov.clientWidth; 
            h = canvas.height = ov.clientHeight; 
        }
        resize();

        var fov = 500;
        var max_depth = 1500;
        var speed = 3.5;
        var num_stars = 1200;

        function mkStar(initZ) {
          var r = Math.random();
          var c = r < 0.58 ? '#D68A18' : (r < 0.97 ? '#20AB7D' : '#3696E3');
          return {
            x: (Math.random() - 0.5) * w * 5,
            y: (Math.random() - 0.5) * h * 5,
            z: initZ ? Math.random() * max_depth : max_depth,
            base_s: Math.random() * 2.5 + 1.5,
            c: c
          };
        }
        
        var stars = [];
        for (var i = 0; i < num_stars; i++) stars.push(mkStar(true));

        var raf = null, running = true;
        function frame() {
          if (!running) return;
          ctx.clearRect(0, 0, w, h);
          
          var cx = w / 2;
          var cy = h / 2;

          for (var i = 0; i < num_stars; i++) {
            var s = stars[i];
            s.z -= speed;
            
            if (s.z <= 0) {
                stars[i] = mkStar(false);
                s = stars[i];
            }
            
            var scale = fov / s.z;
            var px = cx + (s.x * scale);
            var py = cy + (s.y * scale);
            var pSize = s.base_s * scale;

            if (px >= 0 && px <= w && py >= 0 && py <= h) {
                var op = (1 - s.z / max_depth) * 1.5;
                op = Math.min(Math.max(op, 0), 0.95);
                
                ctx.globalAlpha = op;
                ctx.fillStyle = s.c;
                ctx.beginPath();
                ctx.arc(px, py, pSize, 0, Math.PI * 2);
                ctx.fill();
            }
          }
          raf = requestAnimationFrame(frame);
        }
        frame();
        window.addEventListener('resize', resize);

        function dismiss() {
          var el = doc.getElementById('meco-intro-singleton');
          if (!el) return;
          running = false;
          try { cancelAnimationFrame(raf); } catch (e) {}
          el.classList.add('fade');
          setTimeout(function() { if (el && el.parentNode) el.parentNode.removeChild(el); }, 900);
        }
        ov.addEventListener('click', dismiss);

      } catch (e) {}
    })();
    </script>
    """, height=0)


# ════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════
def section_sep():
    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

def credibility_badge(has_real: bool = True, has_sim: bool = False):
    badges = ""
    if has_real:
        badges += ('<span class="badge badge-real"><span class="badge-dot"></span>'
                   'Real data · Jacobs et al. (2025)</span>')
    if has_sim:
        badges += ('<span class="badge badge-sim"><span class="badge-dot"></span>'
                   'Simulated / illustrative</span>')
    st.markdown(f'<div class="badge-row">{badges}</div>', unsafe_allow_html=True)

def build_sankey(replace, enhance, support, label_r, label_e, label_s):
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
        "rgba(168,116,14,0.88)", "rgba(29,140,105,0.85)", "rgba(46,124,184,0.88)",
        "rgba(138,132,123,0.85)", "rgba(138,132,123,0.80)", "rgba(138,132,123,0.80)",
        "rgba(138,132,123,0.80)", "rgba(184,176,164,0.75)", "rgba(61,122,82,0.90)",
    ]
    source = [0,0,0,0,0,0, 1,1,1,1,1,1, 2,2,2]
    target = [3,4,5,6,7,8, 3,4,5,6,7,8, 3,7,8]
    value  = [r_bio, r_dis, r_was, r_fib, r_oth, r_crit,
              e_bio, e_dis, e_was, e_fib, e_oth, e_crit,
              s_bio, s_oth, s_crit]
    link_colors = []
    for s, t in zip(source, target):
        if t == 8:
            link_colors.append("rgba(61,122,82,0.50)" if s == 2 else "rgba(61,122,82,0.20)")
        elif s == 0: link_colors.append("rgba(168,116,14,0.20)")
        elif s == 1: link_colors.append("rgba(29,140,105,0.20)")
        else:        link_colors.append("rgba(46,124,184,0.24)")
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(pad=18, thickness=22, label=nodes, color=node_colors,
                  line=dict(color="#FFFFFF", width=0.5)),
        link=dict(source=source, target=target, value=value, color=link_colors,
                  hovertemplate="%{source.label} → %{target.label}<br>Flow: %{value} units<extra></extra>"),
    ))
    fig.update_layout(paper_bgcolor="#FFFFFF",
                      font=dict(size=11, color="#4A453E", family="Inter, sans-serif"),
                      height=440, margin=dict(l=10, r=10, t=10, b=10))
    return fig


# ════════════════════════════════════════════════════════════════
# SECTION 0 · Feel — compact tag/chip grid
# ════════════════════════════════════════════════════════════════

# Hero-nav + opening-animation CSS.
st.markdown("""
<style>
/* ── Hero navigation ──────────────────────────────────────── */
.hero-nav { display: flex; gap: 10px; align-items: flex-start; flex-wrap: wrap;
            margin-bottom: 1.7rem; }
.hn-primary {
    font: 500 .74rem/1 'Inter', sans-serif; letter-spacing: .02em;
    padding: 9px 16px; border-radius: 20px; text-decoration: none;
    background: rgba(61,122,82,0.10); color: #356B49;
    border: 1px solid rgba(61,122,82,0.40);
    transition: background .18s, border-color .18s;
}
.hn-primary:hover { background: rgba(61,122,82,0.17); border-color: rgba(61,122,82,0.65); }
/* Secondary pill — the researchers' shortcut straight to the Data Sandbox */
.hn-secondary {
    font: 500 .74rem/1 'Inter', sans-serif; letter-spacing: .02em;
    padding: 9px 16px; border-radius: 20px; text-decoration: none;
    background: #FFFFFF; color: #4A453E; border: 1px solid #E5E1DA;
    transition: background .18s, border-color .18s, color .18s;
}
.hn-secondary:hover {
    border-color: rgba(61,122,82,0.45); background: rgba(61,122,82,0.05); color: #2A2722;
}
/* Stop scrolled-to headings from hiding under the top padding */
.sec-anchor { display: block; height: 0; scroll-margin-top: 2rem; }

/* ── One-time opening animation (full-screen overlay injected by JS) ─────── */
.meco-intro {
    position: fixed; inset: 0; z-index: 999999;
    background: #F7F5F1; overflow: hidden; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    opacity: 1; transition: opacity .85s ease;
}
.meco-intro.fade { opacity: 0; }
.meco-intro canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
.meco-intro .intro-center {
    position: relative; z-index: 2; text-align: center; padding: 0 1.5rem;
    opacity: 0; transform: translateY(10px);
    transition: opacity 1s ease .25s, transform 1s ease .25s;
}
.meco-intro.in .intro-center { opacity: 1; transform: translateY(0); }
.meco-intro .intro-n   { font: 700 4.2rem/1.05 'Playfair Display', serif; color: #2A2722; }
.meco-intro .intro-cap { font: 300 1.15rem/1.6 'Inter', sans-serif; color: #6B665E; margin-top: .7rem; }
.meco-intro .intro-legend {
    margin-top: 1.8rem; display: flex; justify-content: center; gap: 24px;
    font: 400 .85rem/1 'Inter', sans-serif; color: #6B665E;
}
.meco-intro .leg-item { display: flex; align-items: center; gap: 8px; }
.meco-intro .leg-dot  { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.meco-intro .intro-skip {
    position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); z-index: 2;
    font: 400 .75rem/1 'Inter', sans-serif; letter-spacing: .2em; text-transform: uppercase; color: #8A847B;
    animation: meco-intro-pulse 2.5s infinite ease-in-out;
}
@keyframes meco-intro-pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
@media (max-width: 640px) {
    .meco-intro .intro-n { font-size: 2.6rem; }
    .meco-intro .intro-legend { flex-direction: column; gap: 12px; align-items: center; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-nav">
  <a class="hn-primary" href="#sec-feel">Take me through the story</a>
  <a class="hn-secondary" href="/explorer" target="_blank">Data Explorer</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-eyebrow">Manufactured Ecosystems · Research Dashboard</div>',
            unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Nature Is Not Optional.</h1>', unsafe_allow_html=True)
st.markdown("""
<p class="hero-sub">
    Over 68,000 scientific papers. Twenty years of research.<br>
    One urgent question: <em>can technology replace what nature provides?</em><br><br>
    Before we show you the data, we want to ask something about your day.
</p>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero-prompt">
    <strong>Tap everything you've already done since you woke up this morning.</strong>
    Small, ordinary things — each one quietly leans on nature.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div id="sec-feel" class="sec-anchor"></div>', unsafe_allow_html=True)

# ── Everyday actions → the ecosystem services they quietly invoke ──
# These mappings are illustrative (NOT from Jacobs et al.): they translate a
# routine action into the bundle of services that make it possible, so readers
# meet the data through their own morning instead of through ES jargon. Every
# service name below must match a name in SERVICES exactly.
_EVERYDAY_ACTIONS = {
    "☕ Drank coffee or tea":                 ["Potable Water", "Pollination", "Soil Formation", "Nutrient Cycling"],
    "🍳 Ate a meal with fresh produce":       ["Food", "Pollination", "Primary Production", "Biodiversity"],
    "👕 Put on cotton or wool clothing":      ["Fibre · Hide · Wood", "Soil Formation", "Nutrient Cycling"],
    "🌬️ Took a deep breath outside":          ["Atmospheric Reg.", "Climate Regulation", "Disease Regulation"],
    "🚰 Washed up or flushed the toilet":     ["Potable Water", "Waste Treatment", "Water Regulation"],
    "💊 Took medication or vitamins":         ["Biochemicals"],
    "⚡ Turned on the heating or AC":          ["Fuel", "Climate Regulation"],
    "🌳 Walked in a park or noticed nature":  ["Aesthetic", "Recreation", "Inspiration · Education"],
    "📦 Used paper or wooden products":       ["Fibre · Hide · Wood", "Primary Production"],
    "🕊️ Felt tied to your local landscape":   ["Cultural Heritage", "Spiritual", "Cultural Identity"],
    "🦋 Saw a bird, insect, or wild animal":  ["Biodiversity", "Pollination", "Coastline Regulation"],
}

# Native pills (Streamlit >= 1.40). Multi-select returns a list of labels.
_selected_actions = st.pills(
    "Everyday actions",
    options=list(_EVERYDAY_ACTIONS.keys()),
    selection_mode="multi",
    label_visibility="collapsed",
) or []

# Map actions → triggered services, then WRITE THE RESULT BACK to session_state
# under each service name. Section 5's data-echo reads st.session_state[name];
# keeping these in sync is what preserves the first/last narrative callback.
_triggered_names = set()
for _act in _selected_actions:
    _triggered_names.update(_EVERYDAY_ACTIONS[_act])
for _name in _svc_names:
    st.session_state[_name] = (_name in _triggered_names)

_all_services_flat0 = [s for cat in SERVICES.values() for s in cat["items"]]
_s0_selected = [s for s in _all_services_flat0 if s["name"] in _triggered_names]
_n0_actions  = len(_selected_actions)
_n0          = len(_s0_selected)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Live counter ──────────────────────────────────────────────
st.markdown(f"""
<div class="ctr">
    <div class="ctr-n">{_n0}</div>
    <div class="ctr-sub">
        hidden ecosystem {"service" if _n0 == 1 else "services"} behind your
        {_n0_actions} routine {"action" if _n0_actions == 1 else "actions"} this morning
    </div>
</div>
""", unsafe_allow_html=True)

# ── Personalised insight panel ───────────────────────────────
if _n0 == 0:
    st.markdown("""
    <div class="insight-empty">
        ↑ Tap at least one everyday action to reveal the unseen natural systems behind your morning.
    </div>
    """, unsafe_allow_html=True)
else:
    _gap0 = [s for s in _s0_selected if s["papers"] < RESEARCH_GAP_THRESHOLD]
    _ok0  = [s for s in _s0_selected if s["papers"] >= RESEARCH_GAP_THRESHOLD]
    _ngap0 = len(_gap0)
    _act_word = "action" if _n0_actions == 1 else "actions"
    if _ngap0 == 0:
        _body0 = (f'Those <span class="hl-green">{_n0_actions}</span> simple {_act_word} quietly rely on '
                  f'<span class="hl-green">{_n0}</span> distinct ecosystem services. '
                  f'The ones behind your morning happen to be relatively well-studied in bio-inspired research. '
                  f"Scroll down to see what happens to the rest.")
    elif _ngap0 == _n0:
        _body0 = (f'You thought you just went about your morning — but those '
                  f'<span class="hl-green">{_n0_actions}</span> {_act_word} invoked '
                  f'<span class="hl-red">{_n0}</span> distinct ecosystem services, and '
                  f'<em>every single one</em> has fewer than {RESEARCH_GAP_THRESHOLD:,} bio-inspired research papers. '
                  f'Science is building technological backups — just not yet for the things <em>you</em> just used.')
    else:
        _body0 = (f'You thought you just went about your morning. In fact those '
                  f'<span class="hl-green">{_n0_actions}</span> {_act_word} quietly invoked '
                  f'<span class="hl-green">{_n0}</span> distinct ecosystem services — and '
                  f'<span class="hl-red">{_ngap0}</span> of them '
                  f'{"has" if _ngap0 == 1 else "have"} fewer than {RESEARCH_GAP_THRESHOLD:,} bio-inspired research papers. '
                  f'If those hidden systems fail, very few technological backup plans currently exist.')
    _gap_tags0 = "".join(f'<span class="tag tag-gap">{s["icon"]} {s["name"]}</span>' for s in _gap0)
    _ok_tags0  = "".join(f'<span class="tag tag-ok">{s["icon"]} {s["name"]}</span>' for s in _ok0)
    _gap_block0 = (f'<div style="margin-bottom:.9rem">'
                   f'<div class="tag-sec-lbl lbl-gap">Research gap — fewer than {RESEARCH_GAP_THRESHOLD:,} papers ({_ngap0})</div>'
                   f'{_gap_tags0}</div>') if _gap0 else ""
    _ok_block0  = (f'<div style="margin-bottom:1.4rem">'
                   f'<div class="tag-sec-lbl lbl-ok">Better researched ({len(_ok0)})</div>'
                   f'{_ok_tags0}</div>') if _ok0 else ""
    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">What the research says about your morning.</div>
        <div class="insight-body">{_body0}</div>
        {_gap_block0}
        {_ok_block0}
        <div class="insight-cta">↓ &nbsp; Scroll to see what 20 years of global research actually looks like</div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# SECTION 1 · Discovery — 68,917 Attempts  
# ════════════════════════════════════════════════════════════════
# section_sep()
st.markdown('<div id="sec-discovery" class="sec-anchor"></div>', unsafe_allow_html=True)
st.markdown('<div class="s1-eyebrow">Section 01 · Discovery</div>', unsafe_allow_html=True)
st.markdown(f'<h2 class="s1-title">{CORPUS["total_papers"]:,} Attempts.</h2>', unsafe_allow_html=True)
st.markdown(f"""
<p class="s1-sub">
    For twenty years, the global scientific community has been working on
    something unprecedented: learning from nature in order to engineer it.
    {CORPUS["total_papers"]:,} published papers. Hundreds of research groups. A shared, if often
    unspoken, question —
    <em style="color:#4A453E; font-style:italic">
    what happens when the natural world can no longer do this on its own?</em>
</p>
<p class="s1-sub">Before we show you the gaps, here is the scale of the effort.</p>
""", unsafe_allow_html=True)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# Build percentages live from the real paradigm totals.
_pt = SVC_SUMMARY["paradigm_totals"]
_pt_total = _pt["replace"] + _pt["enhance"] + _pt["support"]
_pct_replace = round(_pt["replace"] / _pt_total * 100) if _pt_total else 0
_pct_support = round(_pt["support"] / _pt_total * 100) if _pt_total else 0
_n_engaged = sum(1 for s in SVC_SUMMARY["services"] if s["total"] > 0)
_n_total_svc = len(SVC_SUMMARY["services"])

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-val">{CORPUS["non_review"]:,}</span>
    <span class="kpi-label">Non-review papers</span>
    <span class="kpi-note">Of which {CORPUS["decision_y"]:,} describe<br>a technology linked to an ES</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-val">{_n_engaged} / {_n_total_svc}</span>
    <span class="kpi-label">Services engaged</span>
    <span class="kpi-note">Spiritual &amp; Cultural Identity<br>remain entirely out of reach</span>
  </div>
  <div class="kpi-card accent-amber">
    <span class="kpi-val kpi-val-amber">{_pct_replace}%</span>
    <span class="kpi-label">Aim to replace nature</span>
    <span class="kpi-note">The dominant paradigm —<br>stand-alone substitutes for ES</span>
  </div>
  <div class="kpi-card accent-green">
    <span class="kpi-val kpi-val-green">{_pct_support}%</span>
    <span class="kpi-label">Aim to support nature</span>
    <span class="kpi-note">The most ecologically aligned<br>approach, yet heavily marginalized</span>
  </div>
</div>
""", unsafe_allow_html=True)

# (The particle field moved to the one-time full-screen opening animation at
#  the top of the page — see the intro component near the top of this script.)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="s1-bridge">
    This imbalance is not a recent development.
    <em>It has been building for twenty years</em> — and accelerating
    as the climate crisis intensifies the demand for technological solutions.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-label">Biomimetic design paradigms · 2004 – 2025</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)
np.random.seed(42)
_years = list(range(2004, 2026))
_raw_w = np.array([0.80,1.00,1.30,1.70,2.20,2.80,3.50,4.30,5.20,6.00,6.80,7.50,
                   8.00,8.50,9.00,9.50,10.0,10.5,11.0,11.5,11.8,4.50])
_base  = (_raw_w / _raw_w.sum() * CORPUS["decision_y"]).astype(int)
_base  = np.maximum((_base * np.random.uniform(0.94,1.06,len(_years))).astype(int), 5)
_r_frac = np.random.uniform(0.55, 0.61, len(_years))
_s_frac = np.random.uniform(0.026, 0.034, len(_years))
_replace_data = (_base * _r_frac).astype(int)
_support_data = np.maximum((_base * _s_frac).astype(int), 3)
_enhance_data = _base - _replace_data - _support_data

_area_fig = go.Figure()
_area_fig.add_trace(go.Scatter(x=_years, y=_support_data, name="Support  (3%)", mode="lines",
    line=dict(width=0.8, color="#2E7CB8"), fillcolor="rgba(46,124,184,0.55)", stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Support: %{y:,} papers<extra></extra>"))
_area_fig.add_trace(go.Scatter(x=_years, y=_enhance_data, name="Enhance  (39%)", mode="lines",
    line=dict(width=0.8, color="#1D8C69"), fillcolor="rgba(29,140,105,0.42)", stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Enhance: %{y:,} papers<extra></extra>"))
_area_fig.add_trace(go.Scatter(x=_years, y=_replace_data, name="Replace  (58%)", mode="lines",
    line=dict(width=0.8, color="#A8740E"), fillcolor="rgba(168,116,14,0.45)", stackgroup="one",
    hovertemplate="<b>%{x}</b><br>Replace: %{y:,} papers<extra></extra>"))
_area_fig.add_vline(x=2013, line_dash="dot", line_color="rgba(42,39,34,0.20)", line_width=1.2)
_area_fig.add_annotation(x=2013.25, y=0.97, yref="paper",
    text='Fitter (2013):<br>"Can ES be replaced?"',
    font=dict(size=9, color="#6B665E", family="Inter, sans-serif"),
    showarrow=False, xanchor="left", yanchor="top")
_area_fig.add_annotation(x=2021, y=int(_support_data[_years.index(2021)]),
    text="<b>Support: 3%</b><br>Most needed. Least resourced.",
    font=dict(size=10, color="#2E7CB8", family="Inter, sans-serif"),
    showarrow=True, arrowhead=2, arrowcolor="#2E7CB8", arrowwidth=1.2, ax=90, ay=-55,
    bgcolor="rgba(255,255,255,0.92)", bordercolor="rgba(46,124,184,0.35)", borderwidth=1, borderpad=6)
_area_fig.update_layout(
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FBF9F5",
    height=430, margin=dict(l=65, r=25, t=25, b=55), hovermode="x unified",
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                    font=dict(size=11, color="#2A2722", family="Inter, sans-serif")),
    legend=dict(orientation="h", y=1.03, x=0.99, xanchor="right", yanchor="bottom",
                font=dict(size=11, color="#6B665E", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", traceorder="reversed"),
    xaxis=dict(tickmode="linear", dtick=2, tickfont=dict(size=11, color="#8A847B"),
               gridcolor="#ECE8E1", linecolor="#E5E1DA", zeroline=False),
    yaxis=dict(title=dict(text="ES-linked publications per year (simulated)",
                          font=dict(size=11, color="#8A847B")),
               tickfont=dict(size=11, color="#8A847B"), tickformat=",",
               gridcolor="#ECE8E1", linecolor="#E5E1DA", zeroline=False))
st.plotly_chart(_area_fig, use_container_width=True, config={"displayModeBar": False})
st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#B8B0A4;margin-top:.6rem;padding-left:2px;">
    Annual counts modelled from cumulative totals in Jacobs et al. (2025).
    Category proportions — Replace 58%, Enhance 39%, Support 3% — drawn directly from published findings.
    Year-to-year noise (±6%) is simulated for illustration.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#9A938A;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# SECTION 2 · The Gap Map  (bar chart REMOVED → now in Sandbox)
# ════════════════════════════════════════════════════════════════
# section_sep()
st.markdown('<div id="sec-gap" class="sec-anchor"></div>', unsafe_allow_html=True)
st.markdown('<div class="s2-eyebrow">Section 02 · The Gap Map</div>', unsafe_allow_html=True)
st.markdown('<h2 class="s2-title">The Services Nobody Is Building.</h2>', unsafe_allow_html=True)
st.markdown(f"""
<p class="s2-sub">
    Of the {CORPUS["total_papers"]:,} publications, {CORPUS["non_review"]:,} are original research — not reviews.
    A panel of cross-disciplinary experts defined 22 ecosystem services that
    nature provides, then asked: <em>does this paper describe a technology
    that contributes to any of them?</em>
</p>
<p class="s2-sub">
    The answer was yes for <b>{CORPUS["decision_y"]:,} papers</b> — just over half.
    The rest pursue bio-inspiration without connecting to a specific
    ecosystem function. The ring below maps how those {CORPUS["decision_y"]:,} papers
    distribute across the 22 services — and where the foundations of our
    food system, our water cycle, and our cultural identity are left
    almost entirely unaddressed.
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Radial coverage chart (replaces the treemap) ─────────────
# Nightingale "area logic": each spoke's length is the SQRT of its paper count,
# so an 11,079-paper field doesn't make a 58-paper field vanish. Each spoke is
# split into three stacked bands (Support inner · Enhance mid · Replace outer)
# by that service's R/E/S share. Services with 0 papers leave a visible gap.
_CAT_ORDER2 = ["Provisioning", "Regulating", "Supporting", "Cultural"]
_R_COL2 = {"support": "rgba(46,124,184,0.85)",
           "enhance": "rgba(29,140,105,0.82)",
           "replace": "rgba(168,116,14,0.85)"}

# Group by category, then largest→smallest within each group (empties land last).
_ord2 = pd.concat(
    [_df2[_df2["category"] == _c].sort_values("total", ascending=False) for _c in _CAT_ORDER2]
).reset_index(drop=True)

_GROUP_GAP2 = 7.0
_n2 = len(_ord2)

# The 2 zero-paper services draw no bar at all, so they don't need a full
# slot — give them a narrow "marker" slot just wide enough for their dashed
# connector line, and hand the freed angle to the 20 real services. This
# shrinks the dead arc near "Spiritual & Cultural Identity" and makes every
# real spoke slightly wider/denser, so the ring reads as fuller overall.
_EMPTY_SLOT2 = 5.0
_n_empty2 = int((_ord2["total"] == 0).sum())
_n_real2 = _n2 - _n_empty2
_avail2 = 360 - len(_CAT_ORDER2) * _GROUP_GAP2 - _n_empty2 * _EMPTY_SLOT2
_slot_real2 = _avail2 / _n_real2
_wid2 = _slot_real2 * 0.86

_thetas2, _cur2, _prev2 = [], 0.0, None
for _, _r in _ord2.iterrows():
    if _r["category"] != _prev2:
        _cur2 += _GROUP_GAP2
    _this_slot2 = _EMPTY_SLOT2 if _r["total"] == 0 else _slot_real2
    _thetas2.append(_cur2 + _this_slot2 / 2)
    _cur2 += _this_slot2
    _prev2 = _r["category"]

_sup2, _enh2, _rep2 = [], [], []
for _, _r in _ord2.iterrows():
    _t = _r["total"]
    _bl = _t ** 0.5 if _t > 0 else 0.0
    if _t > 0:
        _sup2.append(_bl * _r["support"] / _t)
        _enh2.append(_bl * _r["enhance"] / _t)
        _rep2.append(_bl * _r["replace"] / _t)
    else:
        _sup2.append(0.0); _enh2.append(0.0); _rep2.append(0.0)
_base_e2 = _sup2
_base_r2 = [_s + _e for _s, _e in zip(_sup2, _enh2)]
_maxr2 = _df2["total"].max() ** 0.5

_cd2 = _ord2[["service", "replace", "enhance", "support", "total"]].values.tolist()
_HOV2 = ("<b>%{customdata[0]}</b><br>Total: %{customdata[4]:,} papers<br>"
         "Replace: %{customdata[1]:,}<br>Enhance: %{customdata[2]:,}<br>"
         "Support: %{customdata[3]:,}<extra></extra>")

_radial = go.Figure()
_radial.add_trace(go.Barpolar(
    r=_sup2, theta=_thetas2, base=[0] * _n2, width=[_wid2] * _n2, name="Support",
    marker=dict(color=_R_COL2["support"], line=dict(color="#FFFFFF", width=0.5)),
    customdata=_cd2, hovertemplate=_HOV2))
_radial.add_trace(go.Barpolar(
    r=_enh2, theta=_thetas2, base=_base_e2, width=[_wid2] * _n2, name="Enhance",
    marker=dict(color=_R_COL2["enhance"], line=dict(color="#FFFFFF", width=0.5)),
    customdata=_cd2, hovertemplate=_HOV2))
_radial.add_trace(go.Barpolar(
    r=_rep2, theta=_thetas2, base=_base_r2, width=[_wid2] * _n2, name="Replace",
    marker=dict(color=_R_COL2["replace"], line=dict(color="#FFFFFF", width=0.5)),
    customdata=_cd2, hovertemplate=_HOV2))

# ── Donut geometry via a negative radial floor ──────────────────────
_HOLE2 = 0.38
_R2 = _maxr2 * 1.05                        # outer bound — range ≈ 1.05× the max spoke
_H2 = _R2 * _HOLE2 / (1 - _HOLE2)          # inner floor so r=0 lands at the hole edge

_cat_theta2 = {}
for _c in _CAT_ORDER2:
    _idx2 = [i for i, (_, _r) in enumerate(_ord2.iterrows()) if _r["category"] == _c]
    _cat_theta2[_c] = sum(_thetas2[i] for i in _idx2) / len(_idx2)
_radial.add_trace(go.Scatterpolar(
    r=[-_H2 * 0.55] * len(_CAT_ORDER2),
    theta=[_cat_theta2[_c] for _c in _CAT_ORDER2], mode="text",
    text=[_c.upper() for _c in _CAT_ORDER2],
    textfont=dict(size=12, color="#ADA89E", family="Inter, sans-serif"),
    hoverinfo="skip", showlegend=False))

_empty2 = [i for i, (_, _r) in enumerate(_ord2.iterrows()) if _r["total"] == 0]

for _idx, _ei2 in enumerate(_empty2):
    _real_service_name = _ord2.iloc[_ei2]["service"]
    
    _radial.add_trace(go.Scatterpolar(
        r=[0, _R2 * 0.32], theta=[_thetas2[_ei2]] * 2, mode="lines",
        line=dict(color="rgba(176,90,46,0.35)", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False))
        
    _staggered_r = -_H2 * (0.15 + (_idx % 2) * 0.25)
    
    _radial.add_trace(go.Scatterpolar(
        r=[_staggered_r],  
        theta=[_thetas2[_ei2]], 
        mode="text",
        marker=dict(size=4, color="#B05A2E", symbol="circle-open"),
        text=[f"{_real_service_name}"], # 👈 使用真实名称
        textposition="middle right" if _thetas2[_ei2] < 180 else "middle left",
        textfont=dict(size=9.5, color="#B05A2E", family="Inter, sans-serif"),
        hoverinfo="skip", showlegend=False))

_radial.update_layout(
    polar=dict(
        bgcolor="#FFFFFF", domain=dict(x=[0, 1], y=[0, 1]),
        radialaxis=dict(visible=False, range=[-_H2, _R2]),
        angularaxis=dict(visible=False, rotation=90, direction="clockwise"),
    ),
    paper_bgcolor="#FFFFFF", height=550, margin=dict(l=10, r=10, t=10, b=10),
    showlegend=False,
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                    font=dict(size=11, color="#2A2722", family="Inter, sans-serif")),
)

# ── Chart + side info panel, side by side ────────────────────────
st.markdown('<div class="chart-label">Coverage across all 22 ecosystem services</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)

_chart_col2, _info_col2 = st.columns([2.1, 1], gap="large")
with _chart_col2:
    st.plotly_chart(_radial, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="display:flex; justify-content:center; gap:28px; margin-top:.3rem;
                font:400 .78rem/1 'Inter',sans-serif; color:#6B665E;">
      <span style="display:inline-flex;align-items:center;gap:6px;">
        <span style="width:11px;height:11px;border-radius:2px;background:#2E7CB8;display:inline-block;"></span>
        Support
      </span>
      <span style="display:inline-flex;align-items:center;gap:6px;">
        <span style="width:11px;height:11px;border-radius:2px;background:#1D8C69;display:inline-block;"></span>
        Enhance
      </span>
      <span style="display:inline-flex;align-items:center;gap:6px;">
        <span style="width:11px;height:11px;border-radius:2px;background:#A8740E;display:inline-block;"></span>
        Replace
      </span>
    </div>
    """, unsafe_allow_html=True)
with _info_col2:
    st.markdown("""
    <div class="radial-info-card">
        <div class="radial-info-title">How to read this chart</div>
        <div class="radial-info-body">
            Each spoke is one ecosystem service, grouped into the four families
            named inside the ring. Spoke length follows the
            <b>square root</b> of its paper count — Nightingale's area logic —
            so a field with 11,079 papers doesn't make one with 58 vanish.
            Each spoke splits into three bands: <span class="ib-su">Support</span>,
            <span class="ib-en">Enhance</span>, and <span class="ib-re">Replace</span>,
            by that service's share of each. A missing spoke means zero papers —
            the small dashed gap near the top is
            <b>Spiritual &amp; Cultural Identity</b>.
        </div>
    </div>
    <div class="radial-info-card insight">
        <div class="radial-info-title">Key insight</div>
        <div class="radial-info-body">
            Pollination, soil formation, and nutrient cycling collectively
            underpin global food security. Together they account for just
            <b>796 papers</b> — about <b>7%</b> of what a single service
            (Biochemicals) has attracted.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">The critical gap — food system services</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=True, has_sim=True)
st.markdown("""
<p class="chart-sub-label">
    Pollination, soil formation, and nutrient cycling collectively
    underpin global food security. Together they account for just
    <b>796 papers</b> — about <b>7%</b> of what a single service
    (Biochemicals) has attracted.
</p>
""", unsafe_allow_html=True)
st.markdown("""
<div class="gap-grid">
  <div class="gap-card">
    <span class="gap-icon">🧬</span>
    <div class="gap-svc">Biochemicals</div>
    <span class="gap-n gap-n-ok">11,079</span>
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
        The rarest research topic in the entire 31,559-paper corpus.</div>
    <div class="gap-ratio"><b>1 paper</b> for every 191 in Biochemicals</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Bar chart relocated to the Data Sandbox — gentle pointer for data-minded readers.
st.markdown("""
<p style="font:300 .74rem/1.7 'Inter',sans-serif;color:#9A938A;margin-top:.4rem;padding-left:2px;">
    Want the exact numbers for all 22 services, sorted and filterable?
    <a href="/explorer" target="_blank" style="color:#356B49;font-weight:500;">Open the Data Explorer ↗</a>
    &nbsp;·&nbsp;
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#9A938A;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# SECTION 2.5 · Nature's Voice (The Engineering-Grade Timeline Engine)
# ════════════════════════════════════════════════════════════════

_voice_cutscene_html = """
<script>
(function() {
  try {
    var doc = window.parent.document;
    
    // Idempotency check: Ensure it plays only once per session
    if (doc.mecoVoicePlayed) return;

    if (!doc.getElementById('nv-cutscene-style')) {
        var style = doc.createElement('style');
        style.id = 'nv-cutscene-style';
        style.innerHTML = `
          /* ── 1. Presentation: Fullscreen Canvas ── */
          .nv-overlay {
            position: fixed; inset: 0; z-index: 999999;
            background: #050706; 
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none;
            transition: opacity 1.8s ease, background 2.0s ease;
          }
          .nv-overlay.in { opacity: 1; pointer-events: auto; cursor: pointer; }
          .nv-overlay.blooming { background: radial-gradient(circle at center, #1E3A26 0%, #0A140F 100%); }
          
          .nv-theater { text-align: center; max-width: 600px; padding: 0 20px; position: relative; z-index: 2; margin-top: 60px; }
          
          /* ── 2. Presentation: Decoupled Text Animation (no transition-delay) ── */
          .nv-line { 
            opacity: 0; 
            transform: translateY(15px); 
            transition: opacity 1.2s cubic-bezier(0.25, 0.8, 0.25, 1), transform 1.2s cubic-bezier(0.25, 0.8, 0.25, 1); 
          }
          .nv-line.visible { opacity: 1; transform: translateY(0); }
          
          .nv-l1 { font: italic 400 3.2rem/1.2 'Playfair Display', serif; color: #FFFFFF; margin-bottom: 2rem; }
          .nv-l2 { font: 300 1.1rem/1.6 'Inter', sans-serif; color: #8A847B; }
          .nv-l3 { font: 300 1.1rem/1.6 'Inter', sans-serif; color: #8A847B; margin-bottom: 3rem; }
          .nv-l3 b { color: #E0C589; font-weight: 500; font-size: 1.3rem; }
          .nv-l4 { font: 400 1.6rem/1.4 'Playfair Display', serif; color: #85C29C; }
          
          .nv-skip { position: absolute; bottom: 40px; font: 400 .75rem/1 'Inter', sans-serif; letter-spacing: .2em; text-transform: uppercase; color: #555; animation: nv-pulse 3s infinite ease-in-out; }
          @keyframes nv-pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }

          /* ── 3. Presentation: Clean Bee Positioning ── */
          .nv-bee-container { 
              position: absolute; top: 15%; left: 50%; 
              transform: translateX(-100vw) translateY(50px) scale(0.6); 
              opacity: 0; 
              transition: transform 2.2s cubic-bezier(0.19, 1, 0.22, 1), opacity 1.5s ease; 
          }
          .nv-bee-container.visible { transform: translateX(-50%) translateY(0) scale(1); opacity: 1; }

          .nv-bee { width: 70px; height: 70px; animation: nv-bobbing 3s ease-in-out infinite; position: relative; }
          @keyframes nv-bobbing { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-12px); } }
          .nv-wing { transform-origin: bottom right; animation: nv-flap 0.08s infinite alternate; fill: rgba(255,255,255,0.7); }
          @keyframes nv-flap { 0% { transform: rotate(10deg); } 100% { transform: rotate(-25deg); } }
          
          /* ── 4. Presentation: Expression Change & Blooming ── */
          .nv-mouth-sad { opacity: 1; transition: opacity 0.4s; }
          .nv-mouth-happy { opacity: 0; transition: opacity 0.4s; }
          .nv-flower { opacity: 0; transform: scale(0) rotate(-45deg); transition: all 1.4s cubic-bezier(0.34, 1.56, 0.64, 1); position: absolute; right: -25px; top: 15px; font-size: 2rem; }
          
          .blooming-active .nv-mouth-sad { opacity: 0; }
          .blooming-active .nv-mouth-happy { opacity: 1; }
          .blooming-active .nv-flower { opacity: 1; transform: scale(1) rotate(0deg); }
        `;
        doc.head.appendChild(style);
    }

    var observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        doc.mecoVoicePlayed = true; 
        observer.disconnect();
        playCinematicCutscene(doc);
      }
    }, { threshold: 0.2 });
    
    if (window.frameElement) { observer.observe(window.frameElement); }

    // ── Core Controller ──
    function playCinematicCutscene(doc) {
      var originalOverflow = doc.body.style.overflow;
      doc.body.style.overflow = 'hidden';

      var ov = doc.createElement('div');
      ov.className = 'nv-overlay';
      ov.innerHTML = `
        <div class="nv-bee-container" id="nv-bee">
          <div class="nv-bee">
            <svg viewBox="0 0 60 60" width="70" height="70">
              <ellipse class="nv-wing" cx="25" cy="15" rx="8" ry="16" />
              <ellipse class="nv-wing" cx="33" cy="18" rx="6" ry="13" style="animation-delay: 0.04s" />
              <rect x="10" y="25" width="40" height="22" rx="11" fill="#E0C589"/>
              <rect x="20" y="25" width="6" height="22" fill="#2A2722"/>
              <rect x="32" y="25" width="6" height="22" fill="#2A2722"/>
              <polygon points="10,32 4,36 10,40" fill="#2A2722"/>
              <circle cx="44" cy="32" r="2.5" fill="#2A2722"/>
              <path class="nv-mouth-sad" d="M 43 39 Q 45 36 47 39" stroke="#2A2722" fill="transparent" stroke-width="1.5" stroke-linecap="round"/>
              <path class="nv-mouth-happy" d="M 43 37 Q 45 41 47 37" stroke="#2A2722" fill="transparent" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <div class="nv-flower">🌸</div>
          </div>
        </div>
        <div class="nv-theater">
          <div class="nv-line nv-l1">"I am Pollination."</div>
          <div class="nv-line nv-l2">You wrote 11,079 papers about biochemicals.</div>
          <div class="nv-line nv-l3">You wrote <b>355</b> about me.</div>
          <div class="nv-line nv-l4">With me, one-third of your world blossoms.</div>
        </div>
        <div class="nv-skip">Click anywhere to continue</div>
      `;
      doc.body.appendChild(ov);

      var bee = ov.querySelector('#nv-bee');

      var FADE_OUT_MS = 1800;
      var timers = [];
      var schedule = function(fn, time) {
        var id = setTimeout(fn, time);
        timers.push(id);
      };
      var clearAllTimers = function() {
        for (var i = 0; i < timers.length; i++) {
          clearTimeout(timers[i]);
        }
      };
      var isExiting = false;
      function endCutscene() {
        if (isExiting) return;
        isExiting = true;

        clearAllTimers();

        ov.style.transition = 'opacity 1.8s ease';
        ov.classList.remove('in');

        setTimeout(function() {
          if (ov.parentNode) ov.parentNode.removeChild(ov);
          doc.body.style.overflow = originalOverflow;
        }, FADE_OUT_MS);
      }
      ov.addEventListener('click', endCutscene);

      // ==========================================
      // Director's Script Control Center 
      // ==========================================
      var T = {
        introIn: 200,        // Stage 1: Fade to black
        beeEnter: 1200,      // Stage 2: Bee flies to the center
        
        // Stage 3: Text fades in precisely line by line
        line1: 1400,         
        line2: 2600,         
        line3: 3800,         
        line4: 5200,         // "One-third of your world blossoms"

        bloom: 6500,         // Stage 4: Climax (turns green + blooms + smiles)
        // Stage 5: held indefinitely — dismissed only by click (see above).
      };

      // Execute Timeline
      
      // Scene 1: Cut to black overlay
      schedule(function() { ov.classList.add('in'); }, T.introIn);

      // Scene 2: Bee glides in gracefully and lands in the center
      schedule(function() { bee.classList.add('visible'); }, T.beeEnter);

      // Scene 3: Text flows in at strictly declared time points
      schedule(function() { ov.querySelector('.nv-l1').classList.add('visible'); }, T.line1);
      schedule(function() { ov.querySelector('.nv-l2').classList.add('visible'); }, T.line2);
      schedule(function() { ov.querySelector('.nv-l3').classList.add('visible'); }, T.line3);
      schedule(function() { ov.querySelector('.nv-l4').classList.add('visible'); }, T.line4);

      // Scene 4: Nature's awakening (Background colors, flower blooms, smile appears)
      schedule(function() {
        ov.classList.add('blooming');
        bee.classList.add('blooming-active');
      }, T.bloom);
    }

  } catch (e) {}
})();
</script>
"""
components.html(_voice_cutscene_html, height=0)

# ═════════════════════════════════
# SECTION 3 · Islands of Expertise 
# ════════════════════════════════
# section_sep()
st.markdown('<div id="sec-islands" class="sec-anchor"></div>', unsafe_allow_html=True)
st.markdown('<div class="s3-eyebrow">Section 03 · Islands of Expertise</div>', unsafe_allow_html=True)
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

_NODES3 = {
    "Materials Science":  (-1.05,  0.30, 92, "Replace", "Engineering", "~8,200 papers"),
    "Mech. Engineering":  (-0.80, -0.28, 78, "Replace", "Engineering", "~6,800 papers"),
    "Chemistry":          (-1.18, -0.18, 70, "Replace", "Engineering", "~6,100 papers"),
    "Biomedical Eng.":    (-0.78,  0.52, 60, "Replace", "Engineering", "~5,200 papers"),
    "Computer Science":   (-0.30,  0.05, 34, "Replace", "Bridge",      "~2,700 papers"),
    "Environmental Sci.": ( 1.02,  0.30, 52, "Enhance", "Ecology",     "~4,400 papers"),
    "Biology":            ( 0.82, -0.30, 40, "Support", "Ecology",     "~3,300 papers"),
    "Ecology":            ( 1.18, -0.10, 34, "Support", "Ecology",     "~2,900 papers"),
    "Architecture/Design":( 0.28, -0.18, 24, "Enhance", "Bridge",      "~1,800 papers"),
}
_EDGES3 = [
    # intra-Engineering (solid, strong)
    ("Materials Science", "Mech. Engineering", 0.82),
    ("Materials Science", "Chemistry",          0.76),
    ("Mech. Engineering", "Biomedical Eng.",    0.55),
    ("Chemistry",         "Biomedical Eng.",    0.58),
    # intra-Ecology (solid, strong)
    ("Ecology",            "Biology",            0.78),
    ("Environmental Sci.", "Ecology",            0.70),
    ("Environmental Sci.", "Biology",            0.50),
    # bridge nodes to their nearer cluster (solid, medium)
    ("Computer Science",   "Mech. Engineering",  0.42),
    ("Architecture/Design","Environmental Sci.", 0.30),
    # cross-cluster (dashed, faint — the whole point)
    ("Biology",            "Materials Science",  0.06),
    ("Ecology",            "Mech. Engineering",  0.05),
    ("Computer Science",   "Architecture/Design",0.10),
]
_PAR_COLORS3 = {"Replace":"rgba(168,116,14,0.90)","Enhance":"rgba(29,140,105,0.85)","Support":"rgba(46,124,184,0.88)"}
_PAR_BORDER3 = {"Replace":"#A8740E","Enhance":"#1D8C69","Support":"#2E7CB8"}

st.markdown('<div class="chart-label">Disciplinary co-occurrence network · biomimetics corpus</div>',
            unsafe_allow_html=True)
credibility_badge(has_real=False, has_sim=True)
st.markdown("""
<p class="chart-sub-label">
    Node size = relative publication volume.
    Node colour = dominant design paradigm
    (<span style="color:#A8740E;">replace</span> /
    <span style="color:#1D8C69;">enhance</span> /
    <span style="color:#2E7CB8;">support</span>).
    Solid lines connect disciplines that frequently co-publish; the few
    <b>dashed</b> lines are the rare cross-cluster collaborations.
</p>
""", unsafe_allow_html=True)

_net3 = go.Figure()
# Background cluster zones — pushed apart to emphasize the divide
_net3.add_shape(type="circle", x0=-1.45, y0=-0.70, x1=-0.55, y1=0.80,
                fillcolor="rgba(168,116,14,0.05)",
                line=dict(color="rgba(168,116,14,0.18)", width=1, dash="dot"), layer="below")
_net3.add_annotation(x=-1.00, y=0.88, text="Engineering & Materials",
                     font=dict(size=10, color="rgba(168,116,14,0.70)", family="Inter, sans-serif"),
                     showarrow=False)
_net3.add_shape(type="circle", x0=0.55, y0=-0.62, x1=1.45, y1=0.70,
                fillcolor="rgba(46,124,184,0.05)",
                line=dict(color="rgba(46,124,184,0.18)", width=1, dash="dot"), layer="below")
_net3.add_annotation(x=1.00, y=0.78, text="Ecology & Life Sciences",
                     font=dict(size=10, color="rgba(46,124,184,0.70)", family="Inter, sans-serif"),
                     showarrow=False)
_net3.add_annotation(x=0.0, y=-0.55, text="← the gap →",
                     font=dict(size=11, color="rgba(42,39,34,0.32)", family="Inter, sans-serif"),
                     showarrow=False)

# Edge traces — solid for intra-cluster, dashed for cross-cluster
for (_a, _b, _w) in _EDGES3:
    _x0, _y0 = _NODES3[_a][0], _NODES3[_a][1]
    _x1, _y1 = _NODES3[_b][0], _NODES3[_b][1]
    _is_cross = (_NODES3[_a][4] != _NODES3[_b][4]) and \
                ("Bridge" not in (_NODES3[_a][4], _NODES3[_b][4]))
    if _is_cross:
        _dash = "dash"; _op = 0.22; _wd = 1.0
    else:
        _dash = "solid"; _op = max(0.12, _w * 0.5); _wd = max(0.8, _w * 4.0)
    _net3.add_trace(go.Scatter(
        x=[_x0, _x1, None], y=[_y0, _y1, None], mode="lines",
        line=dict(width=_wd, color=f"rgba(42,39,34,{_op:.2f})", dash=_dash),
        hoverinfo="skip", showlegend=False))

# Node text positions
_TEXT_POS = {
    "Materials Science":   "top center",
    "Mech. Engineering":   "bottom center",
    "Chemistry":           "middle left",
    "Biomedical Eng.":     "top center",
    "Computer Science":    "top center",
    "Environmental Sci.":  "top center",
    "Biology":             "bottom center",
    "Ecology":             "middle right",
    "Architecture/Design": "bottom center",
}
for _par3 in ["Replace", "Enhance", "Support"]:
    _nx, _ny, _nsz, _nlbl, _nhtxt, _ntpos = [], [], [], [], [], []
    for _nname, (_nx_, _ny_, _nsz_, _npar_, _ncl_, _npl_) in _NODES3.items():
        if _npar_ != _par3: continue
        _nx.append(_nx_); _ny.append(_ny_); _nsz.append(_nsz_)
        _nlbl.append(_nname)   # all 9 nodes labelled now — few enough to stay clean
        _ntpos.append(_TEXT_POS.get(_nname, "top center"))
        _nhtxt.append(f"<b>{_nname}</b><br>Dominant paradigm: {_npar_}<br>"
                      f"Cluster: {_ncl_}<br>{_npl_}")
    _net3.add_trace(go.Scatter(
        x=_nx, y=_ny, mode="markers+text", name=_par3,
        text=_nlbl, textposition=_ntpos,
        textfont=dict(size=10, color="#4A453E", family="Inter, sans-serif"),
        hoverinfo="text", hovertext=_nhtxt,
        marker=dict(size=_nsz, color=_PAR_COLORS3[_par3],
                    line=dict(width=1.5, color=_PAR_BORDER3[_par3]))))
_net3.update_layout(
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FBF9F5",
    height=520, margin=dict(l=20, r=20, t=20, b=20), showlegend=True,
    legend=dict(orientation="h", y=-0.04, x=0.5, xanchor="center",
                font=dict(size=11, color="#6B665E", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    hovermode="closest",
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                    font=dict(size=11, color="#2A2722", family="Inter, sans-serif")),
    xaxis=dict(visible=False, range=[-1.65, 1.65]),
    yaxis=dict(visible=False, range=[-0.85, 1.00]))
st.plotly_chart(_net3, use_container_width=True, config={"displayModeBar": False})

# RoboBee case study (unchanged)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">Case study — RoboBee</div>', unsafe_allow_html=True)
credibility_badge(has_real=False, has_sim=True)
components.html("""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; color: #2A2722; }
  .case-wrapper { background: #FFFFFF; border: 1px solid #E5E1DA; border-radius: 12px; padding: 1.6rem 1.8rem; box-shadow: 0 1px 3px rgba(42,39,34,.04); }
  .case-header { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: #2A2722; margin-bottom: .25rem; }
  .case-meta { font-size: .7rem; font-weight: 300; color: #8A847B; margin-bottom: 1.4rem; letter-spacing: .08em; text-transform: uppercase; }
  .case-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 1.1rem; }
  .case-col { background: #FBF9F5; border: 1px solid #E5E1DA; border-radius: 8px; padding: 1.1rem 1rem; }
  .case-col.col-eng  { border-top: 2px solid rgba(168,116,14,0.6); }
  .case-col.col-eco  { border-top: 2px solid rgba(46,124,184,0.6); }
  .case-col.col-both { border-top: 2px solid rgba(61,122,82,0.6); }
  .case-col-title { font-size: .7rem; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .75rem; }
  .col-eng  .case-col-title { color: #8A5E0B; }
  .col-eco  .case-col-title { color: #246592; }
  .col-both .case-col-title { color: #356B49; }
  ul { padding-left: 1.1rem; list-style: disc; }
  ul li { font-size: .75rem; font-weight: 300; line-height: 1.7; color: #6B665E; margin-bottom: .15rem; }
  ul li b { color: #2A2722; font-weight: 500; }
  ul li em { color: #356B49; font-style: italic; }
  .case-footer { font-size: .78rem; font-weight: 300; font-style: italic; line-height: 1.65; color: #8A847B; border-top: 1px solid #E5E1DA; padding-top: .9rem; }
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

# Framing analysis diverging bar (unchanged)
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
    "term": ["Stewardship","Coexistence","Symbiosis","Holistic","Resilience","Restoration","Partnership",
             "Synthetic","Engineering","Control","Extraction","Maximization","Exploitation","Optimization","Substitution"],
    "replace_freq": [-6,-9,-11,-14,-22,-7,-5,-68,-92,-115,-79,-102,-74,-86,-91],
    "support_freq": [44,60,68,50,78,58,40,14,20,10,7,5,4,9,6],
})
_frame3 = go.Figure()
_frame3.add_trace(go.Bar(y=_FRAMING3["term"], x=_FRAMING3["replace_freq"], orientation="h",
    name="Replace subcorpus (technological framing)",
    marker=dict(color="rgba(168,116,14,0.75)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Replace subcorpus: %{customdata:.0f} per 1,000 abstracts<extra></extra>",
    customdata=np.abs(_FRAMING3["replace_freq"])))
_frame3.add_trace(go.Bar(y=_FRAMING3["term"], x=_FRAMING3["support_freq"], orientation="h",
    name="Support subcorpus (ecological framing)",
    marker=dict(color="rgba(46,124,184,0.78)", line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Support subcorpus: %{x:.0f} per 1,000 abstracts<extra></extra>"))
_frame3.add_vline(x=0, line_color="rgba(42,39,34,0.25)", line_width=1)
_frame3.add_annotation(x=-58, y=1.04, yref="paper", text="← Technological / Control",
    font=dict(size=9, color="rgba(168,116,14,0.70)", family="Inter, sans-serif"),
    showarrow=False, xanchor="right")
_frame3.add_annotation(x=58, y=1.04, yref="paper", text="Ecological / Relational →",
    font=dict(size=9, color="rgba(46,124,184,0.70)", family="Inter, sans-serif"),
    showarrow=False, xanchor="left")
_frame3.update_layout(
    barmode="relative", paper_bgcolor="#FFFFFF", plot_bgcolor="#FBF9F5",
    height=520, margin=dict(l=10, r=20, t=30, b=55), hovermode="y unified",
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                    font=dict(size=11, color="#2A2722", family="Inter, sans-serif")),
    legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                font=dict(size=11, color="#6B665E", family="Inter, sans-serif"),
                bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    xaxis=dict(title=dict(text="Occurrences per 1,000 abstracts (simulated)",
                          font=dict(size=11, color="#8A847B")),
               tickfont=dict(size=11, color="#8A847B"),
               tickvals=[-120,-80,-40,0,40,80], ticktext=["120","80","40","0","40","80"],
               gridcolor="#ECE8E1", linecolor="#E5E1DA", zeroline=False),
    yaxis=dict(tickfont=dict(size=11, color="#6B665E", family="Inter, sans-serif"),
               autorange="reversed", linecolor="#E5E1DA", gridcolor="rgba(0,0,0,0)"))
st.plotly_chart(_frame3, use_container_width=True, config={"displayModeBar": False})
st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#B8B0A4;margin-top:.4rem;padding-left:2px;">
    Discipline network is simulated from plausible WoS Categories co-occurrence patterns.
    Framing analysis word frequencies are simulated for illustration.
    RoboBee citation: Jafferis et al. (2019), <em>Nature</em> 570, 491–495.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#9A938A;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════
# SECTION 4 · What 3% Teaches Us  
# ═══════════════════════════════
# section_sep()
st.markdown('<div id="sec-3pct" class="sec-anchor"></div>', unsafe_allow_html=True)
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

_SCENARIOS4 = {
    "Current state  (Support = 3%)": {
        "replace": 580, "enhance": 390, "support": 30,
        "label_r": "Replace  58%", "label_e": "Enhance  39%", "label_s": "Support   3%",
        "callout": ("At <b>3%</b>, Support-oriented research sends only <b>~8 units</b> "
                    "to Critical Services — the rarest, most foundational flows in the entire corpus."),
    },
    "Scenario  (Support = 20%)": {
        "replace": 410, "enhance": 390, "support": 200,
        "label_r": "Replace  41%", "label_e": "Enhance  39%", "label_s": "Support  20%",
        "callout": ("At <b>20%</b>, the flow to Critical Services grows to <b>~70 units</b> — "
                    "a <b>9× increase</b> — while Replace research still receives the majority."),
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
_scenario_key = st.radio(label="Select scenario", options=list(_SCENARIOS4.keys()),
                         horizontal=True, label_visibility="collapsed")
_sc4 = _SCENARIOS4[_scenario_key]
st.markdown(f'<div class="scenario-callout">{_sc4["callout"]}</div>', unsafe_allow_html=True)
_sankey4 = build_sankey(_sc4["replace"], _sc4["enhance"], _sc4["support"],
                        _sc4["label_r"], _sc4["label_e"], _sc4["label_s"])

_sankey4.update_traces(
    textfont=dict(
        size=12, 
        color="#333333",   
        family="Inter, sans-serif"
    )
)
_sankey4.update_layout(
    hoverlabel=dict(
        font=dict(size=13, color="#333333")
    )
)
# ═════════════════════════════════════════════════
st.plotly_chart(_sankey4, use_container_width=True, config={"displayModeBar": False})

# Global accessibility map 
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
    "Country": ["United States","China","Germany","United Kingdom","Canada","Australia",
                "France","Japan","South Korea","Brazil","India","South Africa",
                "Mexico","Kenya","Nigeria","Indonesia"],
    "Region": (["Global North"]*9) + (["Global South"]*7),
    "Replace_Papers": [5200,4800,2100,1800,1200,850,1550,1320,580,350,720,160,140,32,18,95],
    "Open_Access_Pct": [28,22,68,72,48,55,62,35,40,82,34,88,78,95,92,86],
})
_map4 = px.scatter_geo(
    _MAP_DATA4, locations="Country", locationmode="country names",
    size="Replace_Papers", color="Open_Access_Pct", hover_name="Country",
    hover_data={"Country": False, "Region": True, "Replace_Papers": True, "Open_Access_Pct": ":.0f"},
    color_continuous_scale=[[0.0,"#A33216"],[0.35,"#C2742F"],[0.65,"#5A9C6E"],[1.0,"#3D7A52"]],
    range_color=[15,100], color_continuous_midpoint=50, size_max=48,
    labels={"Open_Access_Pct": "Open Access %"})
_map4.update_geos(showcountries=True, countrycolor="rgba(218,213,204,0.9)",
    showcoastlines=True, coastlinecolor="rgba(206,200,189,0.8)",
    showland=True, landcolor="#EFEBE4", showocean=True, oceancolor="#F7F5F1",
    showframe=False, projection_type="natural earth")
_map4.update_layout(paper_bgcolor="#FFFFFF", geo_bgcolor="#FFFFFF",
    height=440, margin=dict(r=0, t=10, l=0, b=0),
    coloraxis_colorbar=dict(title=dict(text="Open Access %", font=dict(size=11, color="#8A847B")),
        tickfont=dict(size=10, color="#8A847B"), ticksuffix="%", thickness=12, len=0.6,
        bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#E5E1DA",
                    font=dict(size=11, color="#2A2722", family="Inter, sans-serif")))
st.plotly_chart(_map4, use_container_width=True, config={"displayModeBar": False})

# ── 3% Spotlight — CAROUSEL (one card at a time, prev/next, dot indicator) ──
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
st.markdown('<div class="chart-label">The 3% — technologies that chose to support</div>',
            unsafe_allow_html=True)

_SPOTLIGHT4 = [
    {"icon":"🦪","title":"Living Shoreline Systems","service":"Coastline Regulation · Supporting","n":"~15",
     "body":"Bio-inspired breakwater structures modelled on oyster reef geometry to dissipate wave energy "
            "while providing substrate for marine organisms. Unlike concrete seawalls, these structures "
            "<em>support</em> the colonisation and growth of natural reef communities over time — the "
            "technology becomes more effective as nature reclaims it."},
    {"icon":"🍄","title":"Mycorrhizal Network Inoculants","service":"Primary Production · Supporting","n":"~8",
     "body":"Fungal network-inspired soil amendments that enhance plant nutrient uptake by inoculating "
            "degraded soils with mycorrhizal consortia. Rather than replacing soil biology, this approach "
            "<em>reactivates</em> dormant underground networks — using the wood-wide web's own logic to "
            "restore carbon sequestration in post-industrial landscapes."},
    {"icon":"🐝","title":"Pollinator Corridor Mapping","service":"Pollination · Supporting","n":"~20",
     "body":"Landscape connectivity models derived from bee foraging algorithms to design habitat corridors "
            "that <em>support</em> existing pollinator populations across fragmented agricultural land. "
            "Unlike RoboBees, this technology asks not how to replace bees — but how to make the landscape "
            "legible to them again."},
    {"icon":"🦫","title":"Beaver-Inspired Wetland Restoration","service":"Water Regulation · Supporting","n":"~12",
     "body":"Low-cost structures modelled on beaver dam geometry to slow water flow, raise water tables, and "
            "restore hydrological function in degraded stream systems. Where beaver populations are locally "
            "extinct, these structures <em>hold space</em> for recolonisation — designed to become redundant "
            "once the living engineer returns."},
]
_n_spot = len(_SPOTLIGHT4)

# Build slide blocks + dots from the data; switching is handled inside the
# component by JS, so the arrows live in the SAME card frame as the content.
_slides_html = ""
for _i, _c in enumerate(_SPOTLIGHT4):
    _hidden = "" if _i == 0 else "hidden"
    _slides_html += f"""
      <div class="mc-slide" {_hidden}>
        <div class="mc-head">
          <div class="mc-icon">{_c['icon']}</div>
          <div>
            <div class="mc-title">{_c['title']}</div>
            <div class="mc-service">{_c['service']}</div>
          </div>
        </div>
        <div class="mc-body">{_c['body']}</div>
        <div class="mc-foot">
          <div><span class="mc-n">{_c['n']}</span><span class="mc-n-label">papers in corpus</span></div>
          <span class="mc-badge">Support</span>
        </div>
      </div>"""

_dots_html = "".join(
    f'<span class="mc-dot{" on" if _i == 0 else ""}"></span>' for _i in range(_n_spot)
)

_carousel_html = """
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .mc-card {
    position: relative; background: #FFFFFF;
    border: 1px solid #E5E1DA; border-top: 2px solid rgba(61,122,82,0.5);
    border-radius: 12px; padding: 1.5rem 3.6rem 1.25rem;
    box-shadow: 0 1px 3px rgba(42,39,34,.04);
  }
  .mc-nav {
    position: absolute; top: 50%; transform: translateY(-50%);
    width: 36px; height: 36px; border-radius: 50%;
    border: 1px solid #E5E1DA; background: #FFFFFF; color: #8A847B;
    font: 400 1.2rem/1 'Inter', sans-serif; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 1px 2px rgba(42,39,34,.05);
    transition: border-color .18s, color .18s, background .18s;
  }
  .mc-nav:hover { border-color: rgba(61,122,82,0.55); color: #356B49; background: rgba(61,122,82,0.06); }
  .mc-nav:active { transform: translateY(-50%) scale(0.93); }
  .mc-prev { left: 12px; }
  .mc-next { right: 12px; }
  .mc-slides { min-height: 184px; }
  .mc-head { display: flex; align-items: flex-start; gap: 12px; margin-bottom: .85rem; }
  .mc-icon { font-size: 1.9rem; line-height: 1; flex-shrink: 0; }
  .mc-title { font: 700 1.1rem/1.25 'Playfair Display', serif; color: #2A2722; }
  .mc-service { font: 500 .62rem/1.4 'Inter', sans-serif; letter-spacing: .14em;
                text-transform: uppercase; color: #356B49; margin-top: 3px; }
  .mc-body { font: 300 .82rem/1.75 'Inter', sans-serif; color: #6B665E; margin-bottom: 1rem; }
  .mc-body em { color: #356B49; font-style: italic; }
  .mc-foot { display: flex; justify-content: space-between; align-items: center;
             padding-top: .8rem; border-top: 1px solid #E5E1DA; }
  .mc-n { font: 700 1.3rem/1 'Playfair Display', serif; color: #2E7CB8; }
  .mc-n-label { font: 300 .62rem/1 'Inter', sans-serif; color: #8A847B; margin-left: 6px; }
  .mc-badge { font: 500 .62rem/1 'Inter', sans-serif; letter-spacing: .12em; text-transform: uppercase;
              padding: 3px 9px; border-radius: 20px; background: rgba(46,124,184,0.10);
              color: #246592; border: 1px solid rgba(46,124,184,0.22); }
  .mc-dots { text-align: center; margin-top: 1rem; }
  .mc-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%;
            margin: 0 4px; background: #DAD5CC; transition: background .18s; }
  .mc-dot.on { background: #3D7A52; }
  .mc-counter { text-align: center; font: 300 .66rem/1 'Inter', sans-serif;
                color: #9A938A; margin-top: .6rem; }
</style></head><body>
<div class="mc-card">
  <button class="mc-nav mc-prev" onclick="mcMove(-1)" aria-label="Previous">&lsaquo;</button>
  <button class="mc-nav mc-next" onclick="mcMove(1)" aria-label="Next">&rsaquo;</button>
  <div class="mc-slides">__SLIDES__</div>
  <div class="mc-dots">__DOTS__</div>
  <div class="mc-counter"><span id="mcCur">1</span> of __N__ &nbsp;&middot;&nbsp; use &lsaquo; &rsaquo; to browse</div>
</div>
<script>
  var mcI = 0;
  var mcSlides = document.querySelectorAll('.mc-slide');
  var mcDots = document.querySelectorAll('.mc-dot');
  function mcRender() {
    for (var j = 0; j < mcSlides.length; j++) { mcSlides[j].hidden = (j !== mcI); }
    for (var k = 0; k < mcDots.length; k++) { mcDots[k].className = 'mc-dot' + (k === mcI ? ' on' : ''); }
    document.getElementById('mcCur').textContent = (mcI + 1);
  }
  function mcMove(d) { mcI = (mcI + d + mcSlides.length) % mcSlides.length; mcRender(); }
  mcRender();
</script>
</body></html>
"""
_carousel_html = (_carousel_html
                  .replace("__SLIDES__", _slides_html)
                  .replace("__DOTS__", _dots_html)
                  .replace("__N__", str(_n_spot)))
components.html(_carousel_html, height=320)

st.markdown("""
<p style="font:300 .68rem/1.7 'Inter',sans-serif;color:#B8B0A4;margin-top:1rem;padding-left:2px;">
    Sankey flow values proportional to published findings in Jacobs et al. (2025).
    Scenario values are illustrative. Global map data is simulated.
    <a href="https://doi.org/10.3390/biomimetics10110784" target="_blank" style="color:#9A938A;">
        Read the full paper →</a>
</p>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# SECTION 5 · You Belong Here   (unchanged)
# ════════════════════════════════════════════════════════════════
# section_sep()
st.markdown('<div id="sec-belong" class="sec-anchor"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">Section 05 · You Belong Here</div>', unsafe_allow_html=True)

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

_all_svc_flat5 = [s for cat in SERVICES.values() for s in cat["items"]]
_selected5 = [s for s in _all_svc_flat5 if st.session_state.get(s["name"], False)]
_gap5 = [s for s in _selected5 if s["papers"] < RESEARCH_GAP_THRESHOLD]
_n_sel5 = len(_selected5); _n_gap5 = len(_gap5)
if _n_sel5 == 0:
    _echo_n = "10"
    _echo_body = "of the 22 services nature provides have fewer than 500 bio-inspired research papers."
    _echo_sub = ("That is not a research gap. That is an open invitation — "
                 "to every scientist, designer, policymaker, artist, and curious human reading this.")
elif _n_gap5 == 0:
    _echo_n = str(_n_sel5)
    _echo_body = ("services you said you depend on today — and all are relatively well-studied. "
                  "But most people's selections aren't.")
    _echo_sub = "10 of the 22 services have fewer than 500 papers. The gap belongs to all of us."
else:
    _gap_names5 = ", ".join(f"<em>{s['name']}</em>" for s in _gap5[:3])
    _more5 = f" and {_n_gap5 - 3} more" if _n_gap5 > 3 else ""
    _echo_n = str(_n_gap5)
    _echo_body = (f"of the {_n_sel5} services you said you depend on today "
                  f"have fewer than 500 bio-inspired research papers — "
                  f"including {_gap_names5}{_more5}.")
    _echo_sub = ("That gap is not abstract. It is the distance between what you need "
                 "and what science is currently building. And it has your name on it.")
st.markdown(f"""
<div class="echo-wrap">
    <span class="echo-n">{_echo_n}</span>
    <p class="echo-label">{_echo_body}</p>
    <p class="echo-sub">{_echo_sub}</p>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

st.markdown('<div class="chart-label">Who are you in this story?</div>', unsafe_allow_html=True)
st.markdown("""
<p style="font:300 .82rem/1.6 'Inter',sans-serif;color:#6B665E;max-width:520px;margin-bottom:1rem;">
    Select the role that feels closest to you.
    We have something to say to each of you.
</p>
""", unsafe_allow_html=True)
_IDENTITIES5 = [
    ("🔬", "Researcher\n/ Scientist", "researcher"),
    ("✏️", "Designer\n/ Engineer", "designer"),
    ("📋", "Policymaker\n/ Funder", "policymaker"),
    ("🎨", "Artist\n/ Writer", "artist"),
    ("📚", "Educator\n/ Student", "educator"),
    ("🌍", "Curious\nHuman", "human"),
]
_cols5 = st.columns(6)
for _col5, (_icon5, _lbl5, _key5) in zip(_cols5, _IDENTITIES5):
    with _col5:
        if st.button(f"{_icon5}  {_lbl5}", key=f"id_{_key5}", use_container_width=True):
            st.session_state.identity = _key5
_RESPONSES5 = {
    "researcher": {
        "title": "The map has your name on it.",
        "body": ("Pollination: <b>355 papers.</b> Nutrient cycling: <b>58 papers.</b> "
                 "Soil formation: <b>343 papers.</b><br><br>"
                 "These are not obscure niches — they are the foundations of global food security. "
                 "They are also among the least-funded, least-published areas in the entire "
                 "bio-inspired corpus. That gap exists not because the questions are unanswerable, "
                 "but because the incentive structures haven't pointed there yet.<br><br>"
                 "<em>Your next paper, your next grant proposal, your next collaboration across "
                 "a disciplinary boundary — that is how the map changes.</em>"),
        "links": [("Read the full paper", "https://doi.org/10.3390/biomimetics10110784"),
                  ("Join the MEco seminar series", "https://www.manufacturedecosystems.com/seminar-series"),
                  ("Explore the project", "https://www.manufacturedecosystems.com/projects")],
    },
    "designer": {
        "title": "Nature is the best brief you have never been given.",
        "body": ("The 3% of bio-inspired research that chooses to <em>support</em> living systems "
                 "rather than replace them — that work needed designers too. "
                 "It needed someone to ask: what does a water system that becomes redundant "
                 "once nature recovers actually look like?<br><br>"
                 "The dominant paradigm — Replace — produces things that can be patented and sold. "
                 "The Support paradigm produces things that work best when they disappear. "
                 "<em>That is a harder, more interesting design problem. "
                 "And it is almost entirely unoccupied.</em>"),
        "links": [("See the virtual exhibition", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
                  ("Call for artists", "https://www.manufacturedecosystems.com/art-apply"),
                  ("Learning from nature", "https://www.manufacturedecosystems.com/home/learning-from-nature")],
    },
    "policymaker": {
        "title": "You hold the dial.",
        "body": ("The reason Critical Services — pollination, soil formation, nutrient cycling — "
                 "have so few research papers is not that scientists don't care. "
                 "It is that <b>funding flows toward what can be patented, commercialised, "
                 "and sold.</b><br><br>"
                 "A single grant program focused on Support-oriented, openly-licensed "
                 "bio-inspired research could shift the entire distribution. "
                 "<em>The lever is small. The effect is large. "
                 "And the decision sits with people like you.</em>"),
        "links": [("Read the research", "https://doi.org/10.3390/biomimetics10110784"),
                  ("About the MEco project", "https://www.manufacturedecosystems.com/about-us"),
                  ("Get in touch", "https://www.manufacturedecosystems.com/contact")],
    },
    "artist": {
        "title": "Imagination shapes what science thinks is possible.",
        "body": ("The Manufactured Ecosystems project was built on a belief that "
                 "this research team holds with conviction: <em>the stories we tell about "
                 "nature — in fiction, in art, in poetry, in film — shape the futures "
                 "that scientists and engineers think are worth building.</em><br><br>"
                 "Your image, your sentence, your character who misses a river that no longer runs — "
                 "that is not separate from the data you have just seen. "
                 "<b>It is the data, felt from the inside.</b><br><br>"
                 "The MEco Anthology is looking for writers. The Exhibition is looking for artists."),
        "links": [("Virtual Exhibition 2025", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
                  ("Call for artists", "https://www.manufacturedecosystems.com/art-apply"),
                  ("Learning from imagination", "https://www.manufacturedecosystems.com/home/learning-from-imagination")],
    },
    "educator": {
        "title": "The silos were built in classrooms. They can be taken down there too.",
        "body": ("The disciplinary isolation we showed you in Section 3 — "
                 "engineers on one island, ecologists on the other — "
                 "was not inevitable. It was constructed, over decades, "
                 "through curricula that trained people to stay in their lanes.<br><br>"
                 "A single course that asks an engineering student and an ecology student "
                 "to design something together — with a shared vocabulary and no clean disciplinary exit — "
                 "<em>that course is already changing the map.</em>"),
        "links": [("Seminar series", "https://www.manufacturedecosystems.com/seminar-series"),
                  ("About the team", "https://www.manufacturedecosystems.com/about-us"),
                  ("MEco projects", "https://www.manufacturedecosystems.com/projects")],
    },
    "human": {
        "title": "You have already done the most important thing.",
        "body": ("You came here. You read this. You thought about which ecosystem services "
                 "you depend on before you had ever heard the phrase "
                 "&ldquo;ecosystem service.&rdquo;<br><br>"
                 "That attention — that willingness to sit with the complexity, "
                 "the data, the gaps, the possibilities — "
                 "<em>that is the rarest thing in the world right now.</em> "
                 "Not expertise. Not funding. Not technology. Attention.<br><br>"
                 "Share this with one person who would find it uncomfortable. "
                 "Ask one question in a meeting that nobody has thought to ask. "
                 "Visit the exhibition. Read the fiction. Come back.<br><br>"
                 "<b>You belong in this conversation.</b> You always did."),
        "links": [("Explore MEco", "https://www.manufacturedecosystems.com"),
                  ("Virtual Exhibition", "https://www.manufacturedecosystems.com/virtual-exhibition-2025"),
                  ("Learning from each other", "https://www.manufacturedecosystems.com/home/learning-from-each-other")],
    },
}
if st.session_state.identity and st.session_state.identity in _RESPONSES5:
    _resp5 = _RESPONSES5[st.session_state.identity]
    _links5 = "".join(f'<a class="r-btn" href="{_url}" target="_blank">{_lbl}</a>'
                      for _lbl, _url in _resp5["links"])
    st.markdown(f"""
    <div class="response-card">
        <div class="response-title">{_resp5["title"]}</div>
        <div class="response-body">{_resp5["body"]}</div>
        <div class="response-actions">{_links5}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="font:300 .8rem/1 'Inter',sans-serif;color:#B8B0A4;
              margin-top:.5rem;font-style:italic;">
        Select a role above to receive a personalised message.
    </p>
    """, unsafe_allow_html=True)
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

st.markdown('<div class="chart-label">Ways to engage with Manufactured Ecosystems</div>',
            unsafe_allow_html=True)
components.html("""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .card { background: #FFFFFF; border: 1px solid #E5E1DA; border-radius: 10px; padding: 1.3rem 1.2rem; text-decoration: none; display: block; box-shadow: 0 1px 3px rgba(42,39,34,.04); transition: border-color .22s, background .22s, box-shadow .22s; }
  .card:hover { border-color: rgba(61,122,82,0.45); background: rgba(61,122,82,0.04); box-shadow: 0 3px 8px rgba(42,39,34,.07); }
  .card-icon { font-size: 1.4rem; display: block; margin-bottom: .6rem; }
  .card-title { font-family: 'Playfair Display', serif; font-size: .92rem; font-weight: 700; color: #2A2722; margin-bottom: .4rem; line-height: 1.25; }
  .card-desc { font-size: .72rem; font-weight: 300; color: #6B665E; line-height: 1.6; margin-bottom: .9rem; }
  .card-cta { font-size: .62rem; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: #3D7A52; }
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

st.markdown("""
<div class="final-wrap">
    <span class="final-you">You</span>
    <span class="final-belong">Belong Here.</span>
    <a class="final-link" href="https://www.manufacturedecosystems.com" target="_blank">
        manufacturedecosystems.com
    </a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
