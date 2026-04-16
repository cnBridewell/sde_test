# Databricks Candidate Pack

This folder contains the Databricks-focused technical task variant for Senior Data Engineer candidates.

## Start Here
1. Read `SeniorDataEngineerTechnicalTask.md`.
2. Bootstrap local PySpark + Delta runtime.
3. Build your pipeline implementation and provide validation evidence for your outputs.

## Quickstart (Concise)
1. Validate runtime with `starter/databricks/local_delta_smoke_test.py`.
2. Build KEV + internal CSV ingestion.
3. Build Bronze/Silver/Gold in Spark.
4. Store Delta tables under a documented warehouse path (recommended: `candidate_pack_databricks/output/warehouse`).
5. Submit validation evidence, reporting output, and strategy write-up.

For local Spark imports and generic managed-table read/write commands, refer to `starter/databricks/README.md` under "Generic Table I/O Pattern".

## Docker Runtime (Any OS)
Preferred when available.

From `candidate_pack_databricks/docker`:

```powershell
docker compose build spark-local
docker compose run --rm spark-local python starter/databricks/local_delta_smoke_test.py
```

Windows convenience wrapper:

```powershell
Set-Location candidate_pack_databricks
.\starter\databricks\bootstrap_local_spark_docker.ps1
```

If Docker CLI exists but build fails, ensure Docker Desktop/daemon is running before retrying.

## Where Output Is Written
- Smoke test result: `candidate_pack_databricks/output/local_smoke/delta_smoke_test_result.json`
- Smoke test warehouse path default: `candidate_pack_databricks/output/warehouse` (override with `DB_WAREHOUSE_DIR`).
- Candidate pipeline Delta table files should use the same warehouse-path convention unless documented otherwise.

## If Docker Is Not Available
Use manual host setup:
1. Install Java 17+.
2. Create a Python 3.10+ virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run `starter/databricks/local_delta_smoke_test.py` locally.
5. Run your pipeline and capture your own validation evidence.

## Key Expectations
- Spark-first implementation.
- Candidate-owned KEV ingestion logic.
- Bronze/Silver/Gold outputs from Spark execution.
- Data quality and observability evidence.
- Databricks strategy note (conceptual, implementation-linked).
- Validation evidence demonstrating non-empty Bronze/Silver/Gold outputs.

## Folder Contents
- `SeniorDataEngineerTechnicalTask.md`
- `requirements.txt`
- `data/`
- `starter/databricks/`
