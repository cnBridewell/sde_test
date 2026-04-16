# Senior Data Engineer Technical Task (Cybersecurity, Databricks Variant)

## Purpose
Assess end-to-end senior data engineering capability in a Databricks-aligned workflow across ingestion, medallion modeling, quality, observability, and reporting.

This variant evaluates two complementary capabilities in one task flow:
- Practical data engineering implementation using PySpark + Delta.
- Databricks platform planning and operational decision quality.

## Software and Access Requirements
- Any OS is acceptable (Windows/macOS/Linux).
- Access to CISA Known Exploited Vulnerabilities (KEV) source data via the public JSON feed: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`.
- Python 3.10+.
- Docker Desktop recommended for local execution.
- Java 17+ on PATH is only required when running Spark directly on host (non-Docker path).
- Execution platform: local PySpark + Delta Lake.
- Databricks platform assessment is conceptual (write-up based), not dependent on live workspace access.
- No paid software is required.

## Task Scenario
Build a cybersecurity exposure lakehouse pipeline that:
1. Ingests vulnerability intelligence from a public feed.
2. Combines it with internal synthetic asset inventory data.
3. Uses the supplied CPE-to-CVE bridge as part of exposure linkage.
4. Produces a stakeholder-usable remediation output for engineering and leadership audiences.

## Delivery Model
This is a single delivery with two complementary evidence streams:
1. **Implementation evidence** from a local PySpark + Delta pipeline.
2. **Databricks platform strategy evidence** from a concise operational write-up.

## Data Sources
### Required public source
- CISA Known Exploited Vulnerabilities (KEV) catalog: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`

You should handle KEV retrieval as part of your ingestion design. If you choose to persist a local snapshot for reproducibility, create and manage that snapshot within your pipeline or setup process.

### Optional public source
- NVD CVE API (JSON)

### Optional enrichment source
- EPSS (Exploit Prediction Scoring System)

EPSS is bonus-only for this variant and not required for core completion.

### Required deterministic linkage source (provided)
- `data/enrichment/cve_cpe_applicability.csv`

`data/enrichment/cve_cpe_applicability_summary.json` is informational only and not required.

### Required internal source (provided synthetic dataset)
- `data/internal_synthetic/assets.csv`
- `data/internal_synthetic/asset_software.csv`

Treat these CSVs as a static input snapshot for the exercise.
Design your implementation as if this data would normally arrive through a routinely scheduled internal ingestion pipeline.

## Quick Execution Summary
1. Confirm runtime works (`local_delta_smoke_test.py`).
2. Ingest KEV and internal CSV sources.
3. Build Bronze/Silver/Gold tables with Spark APIs.
4. Emit validation evidence and run metadata.
5. Produce reporting output plus a short Databricks strategy note.

Implementation may be delivered as either notebooks, Python scripts, or a hybrid approach.

## Delivery Shape (Single Flow)
### Implementation Evidence (primary)
Build and run the PySpark + Delta pipeline end-to-end with Bronze/Silver/Gold outputs.

### Platform Strategy Evidence (embedded)
Alongside implementation artifacts, include a concise write-up explaining how you would operationalize this in Databricks (jobs, governance, cost/performance, failure handling).

This write-up should reference your actual implementation choices, not generic platform notes.

## Mandatory Scope
### 1) Ingestion and Integration
- Pull and normalize data from the live CISA KEV feed as part of your ingestion process.
- Read internal inventory data from provided synthetic sources.
- Normalize nested JSON where needed.
- Make a reasonable decision about whether to persist a reproducible KEV snapshot locally.
- Use `cve_cpe_applicability.csv` to support exposure linkage.

### 2) Medallion Data Modeling (Required)
- Implement Bronze/Silver/Gold layers.
- Define table grain and keys for major Silver and Gold outputs.
- Document key design decisions and tradeoffs.

### 3) Data Quality and Testing
- Implement validation checks for: null keys, duplicate keys, freshness, and basic linkage coverage.
- Add lightweight tests or assertions for critical logic.
- Surface failures clearly.

### 4) Observability and Reliability
- Add basic logging and error handling.
- Emit one run summary artifact with start/end/duration/status and Bronze/Silver/Gold row counts.

### 5) Reporting
- Deliver one stakeholder-facing output with asset exposure context (for example: business unit, criticality, exposure counts, and key summary KPI[s]).

The output should be directly usable by a non-pipeline engineer (for example: security operations lead, remediation manager, or engineering manager).

## Databricks Strategy Note (Required, conceptual)
Provide exactly 3 bullets (maximum 2 lines each). Each bullet must include: decision, rationale, and one implementation-linked reference.
1. Workflow orchestration and idempotency approach.
2. Governance boundaries plus failure/staleness handling approach.
3. Cost/performance approach tied to one Spark or Delta optimization.

## Practical Run Guidance (PySpark + Delta)
Starter tooling is provided in `starter/databricks/` to reduce setup friction:
- `bootstrap_local_spark_docker.ps1`: recommended local runtime bootstrap using Docker (isolated Java + Spark).
- `local_delta_smoke_test.py`: validates local Spark + Delta runtime setup.

For local Spark-specific imports and generic managed-table read/write examples, see `starter/databricks/README.md` ("Generic Table I/O Pattern").

For local execution (inside or outside Docker), Delta table files are managed by Spark in a warehouse path you configure.
Recommended convention: `candidate_pack_databricks/output/warehouse`.
`local_delta_smoke_test.py` configures this same default and reports it in output JSON.
If you choose a different location, document it clearly in your run instructions.

No Bronze/Silver/Gold transformation templates are provided; pipeline design and implementation are part of the assessment.

## Python and Spark Requirements
- Core data transformations must run through Spark APIs.
- Pandas is acceptable for minor convenience steps but not as the main pipeline engine.

## Bonus Track (Optional)
### A) ML Extension
- Build a lightweight model for one of:
  - vulnerability risk scoring/prioritization
  - anomaly detection in exposure patterns
- If you include ML, optionally describe how you would track experiments in MLflow on Databricks.

### B) Platform Polish
- Additional points for reproducible job structure, practical optimization choices, and clear operational notes.

## Expected Deliverables
1. **Implementation package**: notebook/script/hybrid code plus run instructions.
2. **Validation evidence**: proof Bronze/Silver/Gold outputs exist, are non-empty, and are reproducible (for example: schema output, row-count output, and run metadata snippets).
3. **Reporting artifact**: one stakeholder-facing output (table/report/dashboard extract) with exposure context.
4. **Data model notes**: key tables and grain.
5. **Databricks strategy note**: concise implementation-linked plan for jobs, governance, reliability, and cost/performance.

## Submission Guidelines
- Make the core flow runnable with clear setup instructions.
- Provide assumptions and known limitations.
- Include output artifacts so reviewers can assess.
- Include a dependency file and a single command or notebook order for core execution.
- Include a brief AI/tooling usage declaration (what was assisted vs what you manually validated).

## What We Evaluate Most
- Correct and robust source integration.
- Strong medallion modeling and Spark transformation quality.
- Clear data quality strategy.
- Practical observability and operations thinking.
- Reporting usefulness for remediation decision-making.
- Databricks platform fluency through clear and practical operational strategy.

## Out of Scope
- Full production deployment.
- Enterprise IAM/network implementation details.
- Exhaustive ML experimentation.
