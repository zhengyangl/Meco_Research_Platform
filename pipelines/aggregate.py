"""
Aggregation
"""


# In[1]:


import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
 
import pandas as pd
import psycopg2


# In[3]:


# ══════════
# CONFIG
# ══════════
DB_URI = "postgresql://pipeline_user:me_dashboard@127.0.0.1:5432/me_dashboard"
OUTPUT_DIR = Path("dashboard_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# In[11]:


# ═══════════════════════════
# THE 22 ECOSYSTEM SERVICES
# ═══════════════════════════

SERVICES_DEF = [
    ("Biochemicals",            "Provisioning"),
    ("Fibre/Hide/Wood",         "Provisioning"),
    ("Fuel",                    "Provisioning"),
    ("Potable Water",           "Provisioning"),
    ("Food",                    "Provisioning"),
    ("Biodiversity",            "Provisioning"),
    ("Disease Regulation",      "Regulating"),
    ("Waste Treatment",         "Regulating"),
    ("Climate Regulation",      "Regulating"),
    ("Atmospheric Regulation",  "Regulating"),
    ("Water Regulation",        "Regulating"),
    ("Pollination",             "Regulating"),
    ("Coastline Regulation",    "Regulating"),
    ("Primary Production",      "Supporting"),
    ("Soil Formation",          "Supporting"),
    ("Nutrient Cycling",        "Supporting"),
    ("Inspiration/Education",   "Cultural"),
    ("Aesthetic",               "Cultural"),
    ("Recreation",              "Cultural"),
    ("Cultural Heritage",       "Cultural"),
    ("Spiritual",               "Cultural"),
    ("Cultural Identity",       "Cultural"),
]
VALID_SERVICES = {name for name, _ in SERVICES_DEF}
SERVICE_TO_CATEGORY = dict(SERVICES_DEF)


# In[12]:


# ════════
# Helper
# ════════
def write_json(path: Path, payload: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


# In[13]:


# ═══════════════════════
# STEP 0 Connect
# ═══════════════════════

t0 = time.time()
conn = psycopg2.connect(DB_URI)


# In[14]:


# ════════════════════════════════════════════════════════════════
# STEP 1 corpus_meta.json — top-level funnel
# ════════════════════════════════════════════════════════════════
 
# All three numbers come from a single query so they are guaranteed
# to be consistent with each other (no race between separate queries).
meta_sql = """
SELECT
    COUNT(*)                                                       AS total_papers,
    COUNT(*) FILTER (WHERE is_review = FALSE)                      AS non_review,
    COUNT(*) FILTER (WHERE is_review = TRUE)                       AS reviews
FROM papers
"""
meta_df = pd.read_sql(meta_sql, conn)
total      = int(meta_df["total_papers"][0])
non_review = int(meta_df["non_review"][0])
reviews    = int(meta_df["reviews"][0])
 
# Decision=Y count needs the classifications join
decision_y_sql = """
SELECT COUNT(*) AS decision_y
FROM papers p
JOIN classifications c ON p.wos_id = c.wos_id
WHERE p.is_review = FALSE
  AND c.is_current = TRUE
  AND c.decision = 'Y'
  AND c.ecosystem_service = ANY(%s)
"""
decision_y_df = pd.read_sql(decision_y_sql, conn, params=(list(VALID_SERVICES),))
decision_y = int(decision_y_df["decision_y"][0])

version_sql = "SELECT version FROM datasets ORDER BY import_date DESC LIMIT 1"
version_df = pd.read_sql(version_sql, conn)
dataset_version = version_df["version"][0] if len(version_df) else None
 
meta = {
    "total_papers":                      total,
    "non_review":                        non_review,
    "reviews":                           reviews,
    "decision_y":                        decision_y,
    "decision_y_pct_of_non_review":      round(decision_y / non_review, 4) if non_review else 0.0,
    "n_services":                        len(SERVICES_DEF),
    "dataset_version":                   dataset_version,
    "generated_at":                      datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
write_json(OUTPUT_DIR / "corpus_meta.json", meta)
print(f"  total={total:,}  non_review={non_review:,}  decision_y={decision_y:,}")


# In[15]:


# ══════════════════════════════════════════════════════
# STEP 2 services_summary.json — 22 services × R/E/S
# ══════════════════════════════════════════════════════
 
# One row per (ecosystem_service, category) combo, filtered to non-review
# Y papers in the whitelist.
svc_sql = """
SELECT
    c.ecosystem_service,
    c.category,
    COUNT(*) AS n
FROM papers p
JOIN classifications c ON p.wos_id = c.wos_id
WHERE p.is_review = FALSE
  AND c.is_current = TRUE
  AND c.decision = 'Y'
  AND c.ecosystem_service = ANY(%s)
GROUP BY c.ecosystem_service, c.category
"""
raw = pd.read_sql(svc_sql, conn, params=(list(VALID_SERVICES),))
 
# Pivot to wide form: one row per service, three columns (R/E/S)
pivot = raw.pivot_table(
    index="ecosystem_service",
    columns="category",
    values="n",
    aggfunc="sum",
    fill_value=0,
).rename_axis(columns=None)
 
# Make sure all three columns exist even if a paradigm is empty for some service
for col in ("Replace", "Enhance", "Support"):
    if col not in pivot.columns:
        pivot[col] = 0
 
# Build the services list in the canonical SERVICES_DEF order. Any service
# defined but with zero papers (e.g. Spiritual, Cultural Identity) appears
# as a real row with zeros.

services_list = []
for svc_name, svc_category in SERVICES_DEF:
    if svc_name in pivot.index:
        row = pivot.loc[svc_name]
        replace_n = int(row["Replace"])
        enhance_n = int(row["Enhance"])
        support_n = int(row["Support"])
    else:
        replace_n = enhance_n = support_n = 0
    services_list.append({
        "service":  svc_name,
        "category": svc_category,
        "total":    replace_n + enhance_n + support_n,
        "replace":  replace_n,
        "enhance":  enhance_n,
        "support":  support_n,
    })
 
# Category-level and paradigm-level rollups
category_totals = {}
paradigm_totals = {"replace": 0, "enhance": 0, "support": 0}
for s in services_list:
    category_totals[s["category"]] = category_totals.get(s["category"], 0) + s["total"]
    paradigm_totals["replace"] += s["replace"]
    paradigm_totals["enhance"] += s["enhance"]
    paradigm_totals["support"] += s["support"]
 
summary = {
    "services":         services_list,
    "category_totals":  category_totals,
    "paradigm_totals":  paradigm_totals,
    "grand_total":      sum(s["total"] for s in services_list),
    "generated_at":     datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
write_json(OUTPUT_DIR / "services_summary.json", summary)
 
# Sanity check
assert summary["grand_total"] == decision_y, (
    f"Mismatch: grand_total={summary['grand_total']} vs decision_y={decision_y}. "
    "Likely cause: ecosystem_service value in classifications not in SERVICES_DEF."
)
print(f"  Services with data: {sum(1 for s in services_list if s['total'] > 0)} / {len(services_list)}")
print(f"  Grand total: {summary['grand_total']:,}  (== decision_y ✓)")
print(f"  Paradigms — Replace: {paradigm_totals['replace']:,}  "
      f"Enhance: {paradigm_totals['enhance']:,}  Support: {paradigm_totals['support']:,}")


# In[16]:


# ════════════════════════════════════════════════════════════════
# STEP 3 papers_classified.parquet — explorer-grade row-level data
# ════════════════════════════════════════════════════════════════
 
papers_sql = """
SELECT
    p.wos_id,
    p.doi,
    p.title,
    p.pub_year,
    p.source_title,
    p.times_cited,
    p.open_access,
    p.authors,
    p.affiliations,
    p.wos_categories,
    p.keywords,
    p.addresses,
    p.funding_orgs,
    c.category,
    c.ecosystem_service,
    c.technology
FROM papers p
JOIN classifications c ON p.wos_id = c.wos_id
WHERE p.is_review = FALSE
  AND c.is_current = TRUE
  AND c.decision = 'Y'
  AND c.ecosystem_service = ANY(%s)
"""
papers_df = pd.read_sql(papers_sql, conn, params=(list(VALID_SERVICES),))
 
# Add the 4-family category derived from the whitelist mapping.
papers_df["service_category"] = papers_df["ecosystem_service"].map(SERVICE_TO_CATEGORY)
 
# Column order for the explorer
COLUMN_ORDER = [
    "wos_id", "doi", "title", "pub_year",
    "source_title", "times_cited", "open_access",
    "authors", "affiliations", "wos_categories",
    "keywords", "addresses", "funding_orgs",
    "category", "ecosystem_service", "service_category", "technology",
]
papers_df = papers_df[COLUMN_ORDER]
 
# Cast pub_year/times_cited to nullable Int (so missing values become <NA>
# instead of NaN floats — cleaner for the Streamlit explorer).
papers_df["pub_year"]    = papers_df["pub_year"].astype("Int64")
papers_df["times_cited"] = papers_df["times_cited"].astype("Int64")
 
# Sanity
assert len(papers_df) == decision_y, (
    f"Row count mismatch: parquet={len(papers_df)} vs decision_y={decision_y}"
)
 
parquet_path = OUTPUT_DIR / "papers_classified.parquet"
papers_df.to_parquet(parquet_path, compression="snappy", index=False)
 
size_mb = os.path.getsize(parquet_path) / (1024 * 1024)
print(f"  Rows: {len(papers_df):,}")
print(f"  Cols: {len(papers_df.columns)}  -> {COLUMN_ORDER}")
print(f"  Size: {size_mb:.1f} MB (snappy-compressed parquet)")


# In[17]:


# ═════════════════
# Done
# ═════════════════
conn.close()
elapsed = time.time() - t0
print(f"\n✓ All files written to {OUTPUT_DIR.resolve()}/")
for fname in ("corpus_meta.json", "services_summary.json", "papers_classified.parquet"):
    fpath = OUTPUT_DIR / fname
    size = os.path.getsize(fpath) / 1024  # KB
    unit = "KB" if size < 1024 else "MB"
    val  = size if size < 1024 else size / 1024
    print(f"  {fname:32s} {val:>7.1f} {unit}")
print(f"\n  Total elapsed: {elapsed:.1f}s")
