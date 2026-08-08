# MEco Research Platform

**"Nature Is Not Optional."**

An interactive research dashboard exploring how biomimetics and bio-inspired
technologies replace, enhance, or support the 22 ecosystem services people
depend on — built on GPT-4.1–annotated classifications of Web of Science
literature, following the framework of Jacobs et al. (2025).

The dashboard is the visible face of a larger **Living Data Asset**: an
automated data engine (ingestion → LLM classification → NLP feature
extraction → aggregation) that keeps the underlying research corpus
growing and versioned over time. See
[`documents/architecture_overview.md`](documents/architecture_overview.md)
for the full system design, database schema, and data lineage model.

---

## What's in the dashboard

| Page | File | Description |
|---|---|---|
| **Narrative** | `app3.0.py` | The main landing page — a guided story through the corpus: funnel metrics, R/E/S (Replace/Enhance/Support) breakdown across ecosystem services, and framing analysis. Loads instantly from pre-computed JSON. |
| **Data Explorer** | `pages/explorer.py` | A full interactive database of ~31,559 classified papers with multi-dimensional filtering (ecological focus, time/impact, publication details, geography/institutions, technology/funding), quick search, shareable URL state, impact-tier cards, and linked visualizations. See [`pages/explorer_feature_list.txt`](pages/explorer_feature_list.txt) for the complete feature list. |

## Repository layout

```
.
├── app3.0.py                  # Narrative page (main Streamlit entry point)
├── pages/
│   ├── explorer.py            # Data Explorer (multi-page Streamlit app)
│   ├── explorer_feature_list.txt
│   └── explorer_older*.py     # Prior iterations, kept for reference
├── pipelines/
│   ├── ingest_initial.py      # Raw WoS/GPT export → PostgreSQL ingestion
│   ├── text_analysis.py       # NLP feature extraction → paper_features table
│   └── aggregate.py           # DB → dashboard_data/ (JSON + Parquet exports)
├── dashboard_data/            # Pre-computed data consumed by the dashboard
│   ├── abstracts.parquet
│   ├── papers_classified.parquet
│   ├── corpus_meta.json / services_summary.json / framing.json / ...
│   └── discovery_data/        # WoS category/co-occurrence discovery outputs
├── llm_validation/            # LLM classification validation scripts
├── documents/
│   └── architecture_overview.md  # Full platform architecture & DB design
├── older_apps/                # Earlier full-app prototypes, kept for reference
├── .streamlit/config.toml     # Streamlit UI config
└── requirements.txt           # Dashboard-only dependencies (lightweight)
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app3.0.py
```

The Data Explorer page (`pages/explorer.py`) is picked up automatically by
Streamlit's multi-page app support once the main app is running.

> Note: `requirements.txt` covers dashboard dependencies only. The pipeline
> scripts in `pipelines/` additionally require `psycopg2` and a running
> PostgreSQL instance — they are run separately on the data-processing side,
> not as part of the dashboard deployment.

## Data pipeline (high level)

```
Raw WoS export (Google Drive)
        ↓
Ingestion & validation  (pipelines/ingest_initial.py)
        ↓
LLM classification (incremental — only new papers are processed)
        ↓
NLP feature extraction  (pipelines/text_analysis.py)
        ↓
PostgreSQL  (papers, classifications, paper_features, audit logs)
        ↓
Aggregation  (pipelines/aggregate.py → dashboard_data/*.json, *.parquet)
        ↓
Streamlit dashboard (app3.0.py + pages/explorer.py)
```

Every classification and derived feature is versioned and traceable back to
its source dataset batch, model version, and prompt version — full details
in [`documents/architecture_overview.md`](documents/architecture_overview.md).

## Corpus snapshot

As of the latest processed batch (`dashboard_data/corpus_meta.json`):

- **68,917** total papers ingested
- **59,599** non-review papers
- **31,559** classified as relevant (biomimetic/nature-inspired) — **52.95%** of non-review papers
- **22** ecosystem services tracked across 4 service families

## Tech stack

Streamlit · Plotly · pandas · NumPy · PyArrow · streamlit-aggrid · PostgreSQL · GPT-4.1 (classification) · gspread (feedback logging)
