# Research Data Platform — Architecture Overview

*Planning document · May 2026 · Julian*

---

## 1. The Vision & Philosophy

While the interactive dashboard is the visible face of this project, it is only the tip of the iceberg. The platform is built as a Living Data Asset. The true long-term value lies in the automated data engine underneath—a curated, ever-growing, and highly structured database of research that the lab can compound and build upon for years.

**Modular by Design (Future-Proofing)**

To ensure the platform outlives current technology trends, the architecture is strictly decoupled. Three core layers were designed to be upgraded independently without breaking the system:

- The Data Source: We are starting with Web of Science, but new APIs (like Scopus or OpenAlex) can be plugged into the ingestion pipeline later without rebuilding the database.
- The AI Engine: The LLM provider, prompt engineering, and taxonomy will inevitably evolve. The system versions every classification, ensuring new models can be applied while historical results are safely preserved.
- The Front-End: Streamlit is the perfect delivery mechanism today, but the underlying data contracts (JSON/Parquet) mean the UI can be entirely swapped out for a different web framework in the future.


---

## 2. Project Architecture

```
Raw data (WoS CSV on Google Drive)
        ↓
Ingestion — standardize the data format
        ↓
Validation — lightweight sanity checks (match rate, year range, required fields)
        ↓
Processing — deduplication, detect new papers, LLM classification
        ↓
Audit — log every classification result with model version + prompt version
        ↓
PostgreSQL database — papers, classifications, paper_features, audit logs
        ↓
Feature Engineering — NLP/PySpark extraction of countries, institutions, topics (writes to paper_features table — versioned, replaceable, never alters core facts)
        ↓
Aggregation — compute stats and exports for the front end
        ↓
Streamlit dashboard (Front End: Two independent paths)
  ├── 1. Aggregation → pre-computed JSON → Narrative page (app.py)
  └── 2. PostgreSQL  → real-time query   → Data Explorer (pages/explorer.py)
        ↓
Embedded in ME website via iframe

```
**Key Architectural Decisions**

1. The Validation Layer: A lightweight check sits right after ingestion. If a raw file fails basic sanity tests (merge match rate < 99.9%, publication years outside 1900–present, missing critical fields), the pipeline halts before any dirty data can contaminate the production database. This is not a heavy infrastructure layer — just a handful of assertions in sources.py.
2. Facts vs. Derivations (Two-Layer Schema): The papers table stores raw, stable facts (title, year, citations, journal). NLP-derived features (extracted country, institution clusters, topic labels) live in a separate paper_features table — versioned the same way classifications are. When NLP methods evolve, you can re-run feature extraction without altering the core facts.
3. Two Independent Dashboard Paths: The Narrative page reads static JSON (loads instantly). The Data Explorer queries live data (flexible filtering and pivoting). These paths share data but not failure modes.

> Each layer is independent. A future student can swap out the dashboard without touching the database, or add a new data source without rewriting the pipeline.


## 3. The Day-to-Day Workflow (For the Research Team)

You don't need to be an engineer or write a single line of code to keep this platform alive. Everything happens automatically. Here is what the actual day-to-day workflow looks like for the team:

1. The Drop. A researcher exports the latest papers from Web of Science (or other platforms) and simply drops the raw Excel file into a shared Google Drive folder. That’s it. You are done.
2. The Invisible Assistant. While the team is offline (e.g., Sunday at midnight), the cloud server quietly wakes up and checks that folder for anything new.
3. The Smart Filter. The system is smart enough to know what it has already read. It sifts out only the brand-new papers and sends them to the LLM for deep reading and classification. The existing, historical database remains completely untouched and perfectly safe.
4. The Morning-After Reveal. By Monday morning, the database and all summary files are securely updated. When the lab logs into the Dashboard, the new papers are already there, fully classified, with the funnel metrics and Explorer seamlessly reflecting the absolute latest scientific landscape.

In short: You drag and drop a file. The machine takes care of the rest.


---

## 4. Database design

- Saves Money: It only processes new papers. You don't pay the AI to read old papers again.
- Never Loses Data: When you use a better AI model later, it saves the new results but keeps the old ones.
- Easy to Fix Mistakes: It records every AI prompt and answer. If the AI makes a mistake, you can easily find out why.
- Fast Dashboard: It separates hard facts from AI opinions, which makes your Streamlit dashboard load instantly.
- Replaceable Features: NLP-derived attributes live in their own table, so re-running extraction with a better method never touches the underlying facts.

```sql
-- Track which batch each paper came from
CREATE TABLE datasets (
    dataset_id   SERIAL PRIMARY KEY,
    source       TEXT,            -- 'WoS', 'Scopus', etc.
    version      TEXT,            -- e.g. '2026-05'
    import_date  TIMESTAMPTZ DEFAULT NOW(),
    record_count INT
);

-- One row per paper (raw facts only)
CREATE TABLE papers (
    wos_id         TEXT PRIMARY KEY,   -- e.g. 'WOS:001382596900001'
    doi            TEXT,                -- nullable, 4.1% of papers have no DOI
    dataset_id     INT REFERENCES datasets(dataset_id),
    title          TEXT,
    abstract       TEXT,
    keywords       TEXT,
    pub_year       INT,
    addresses      TEXT,
    funding_orgs   TEXT,
    wos_categories TEXT,
    is_review      BOOLEAN,
    source_title   TEXT,                -- Journal name
    times_cited    INT,                 -- Core citation count
    open_access    TEXT,                -- OA status (e.g., 'Open Access', 'Closed')
    authors        TEXT,                -- Full author names
    affiliations   TEXT                 -- Cleaned institution lists
);

-- Classification results -- versioned so history is never lost
CREATE TABLE classifications (
    classification_id SERIAL PRIMARY KEY,
    wos_id            TEXT REFERENCES papers(wos_id),
    run_id            UUID,
    model_version     TEXT,
    prompt_version    TEXT,
    decision          CHAR(1),     -- Y / N
    category          TEXT,        -- Replace / Enhance / Support
    ecosystem_service TEXT,
    technology        TEXT,
    is_current        BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- Only one "current" result per paper allowed
CREATE UNIQUE INDEX idx_one_current_per_paper
    ON classifications (wos_id)
    WHERE is_current = TRUE;

-- NLP-derived features -- kept separate so methods can evolve
-- without altering core facts. Same versioning pattern as classifications.
CREATE TABLE paper_features (
    feature_id   SERIAL PRIMARY KEY,
    wos_id       TEXT REFERENCES papers(wos_id),
    feature_set  TEXT,              -- e.g. 'nlp_v1', 'topics_bertopic_v2'
    feature_key  TEXT,              -- e.g. 'country', 'topic_cluster', 'institution_normalised'
    feature_val  TEXT,
    is_current   BOOLEAN DEFAULT TRUE,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_features_current
    ON paper_features (wos_id, feature_key)
    WHERE is_current = TRUE;

-- Full audit trail -- every LLM call is logged
CREATE TABLE classification_audit (
    id             SERIAL PRIMARY KEY,
    wos_id         TEXT,
    model_name     TEXT,
    model_version  TEXT,
    prompt_version TEXT,
    raw_output     JSONB,
    confidence     FLOAT,
    run_id         UUID,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- Pipeline run log -- useful when something goes wrong
CREATE TABLE pipeline_runs (
    run_id           UUID PRIMARY KEY,
    start_time       TIMESTAMPTZ,
    end_time         TIMESTAMPTZ,
    papers_processed INT,
    papers_failed    INT,
    model_version    TEXT,
    prompt_version   TEXT,
    git_commit_hash  TEXT
);
```

## 5. End-to-End Data Lineage
Every number on the dashboard can be traced back to its raw file origin through explicit database keys. This is what makes the platform scientifically defensible: if any figure is challenged during peer review, the exact provenance is one query away.

```
[ Raw WoS Export File ]
           │
           ▼
  (datasets.version: '2026-05')
           │
           ▼
[ Individual Paper Record ]  <── (papers.dataset_id)
     Primary Key: wos_id
           │
           ├────────────────────────────────── ───┐
           │                                         │
           ▼                                         ▼
(classifications.run_id)                (paper_features.feature_set)
           │                                         │
           ▼                                         ▼
[ classification_audit ]                  [ Extracted Attributes ]
  - exact prompt                            - country
  - model_version                           - institution
  - raw_output JSON                         - topic_cluster
           │                                         │
           └───────────────────┬─────────────────┘
                               │
                               ▼
                [ Dashboard Metrics / Explorer ]
```
If a classification is questioned, a researcher can input the paper's wos_id and instantly retrieve:
- the exact dataset batch the paper came from,
- the prompt and model version that produced the classification,
- the raw JSON response received from the LLM,
- which feature-extraction method generated any derived attributes shown.

## 6. Where computation happens

All computationally heavy tasks, like running the LLM and writing to the database, take place on a cloud server. GitHub Actions only handles the lightweight stuff: detecting new files, triggering the pipeline, and updating the dashboard. The LLM never runs inside GitHub Actions because it leads to timeouts, rate limits, and messy handovers. Here is how the workload is split:

```
Server (cloud)            │    GitHub Actions
-────────────────────── │──────────────────
LLM classification        │    Detect new data
Deduplication             │    Trigger pipeline
NLP feature extraction    │    Pull updated JSON
Write to PostgreSQL       │    Redeploy dashboard
Generate summary JSON     │    
```

---

## 7. Incremental processing

Old papers are never re-processed unless there's a deliberate reason (like upgrading the model). Each pipeline run only touches new wos_ids:

```
Example: 60,000 existing papers + 300 new ones → only the 300 new ones get classified.
```
The "what to process" logic is simple: query for wos_ids that don't yet have an is_current = TRUE row in classifications. If the pipeline crashes mid-run, the next run picks up exactly where it left off — no duplicate API billing, no special state-machine fields needed. The same pattern applies to paper_features.
This keeps costs low and run times short as the corpus grows.


---

## 8. Pipeline Outputs & Data Interfaces
The `aggregate.py` script bridges the database and the Streamlit front end. It is responsible for generating completely hard-code-free data files for the dashboard.

1. Narrative Page Dependencies (JSON) 
The narrative page must start up instantly and will read directly from these two generated files:
- services_summary.json: Contains the breakdown of the 22 ecosystem services and their Replace/Enhance/Support (R/E/S) absolute counts.
- corpus_meta.json: Contains top-level metrics, e.g., {"total": 68917, "non_review": 59599, "decision_y": 31559, "updated": "2026-06"}.

2. Data Explorer Interface (explorer.py) 
To manage Streamlit Cloud's connection limits and security, the explorer page will be rolled out in two phases:
- Phase 1: aggregate.py generates a static papers_classified.parquet file (e.g., 31,559 rows containing wos_id, doi, title, pub_year, category, ecosystem_service, technology, times_cited, open_access, source_title, authors,plus current NLP-derived features joined in from paper_features). The explorer reads this local file for fast, offline filtering. Deploying this is simple and doesn't rely on the database being online.
- Phase 2 (Long-term Target): The explorer transitions to using st.connection to query the PostgreSQL database directly. This provides maximum flexibility but requires configuring secure network routing between Streamlit Cloud and the EC2 database instance.




## 9. Codebase layout

```
repo/
├── pipeline/
│   ├── sources.py           # Data ingestion + validation
│   ├── classify.py          # LLM classification, incremental processing
│   ├── text_analysis.py     # NLP feature extraction → paper_features
│   ├── aggregate.py         # Computes stats → outputs dashboard_data/
│   └── run_pipeline.py      # Entry point
├── app.py                   # Narrative page (Main Streamlit app)
├── pages/
│   └── explorer.py         # Data Explorer (Multi-page app)
├── dashboard_data/         # Pre-computed JSON & Parquet, checked into Git
├── requirements.txt            # Dashboard dependencies only (lightweight)
├── requirements_pipeline.txt   # Pipeline + LLM libraries
├── .github/workflows/
│   └── deploy.yml              # Orchestration + deployment only (No LLM)
└── docs/
    ├── index.md                # Start here
    ├── architecture.md
    ├── data_dictionary.md
    ├── data_schema_supplement.md
    ├── handover.md             # How to update the database
    └── prompt_specification.md # Exact LLM prompt + version history

```
* Every part of the system will be documented, so a student joining in a year or two can make updates without needing to reverse-engineer anything.
