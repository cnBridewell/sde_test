# Databricks Starter Pack

This folder provides optional scaffolding for candidates completing the Databricks variant.

## Files
- `bootstrap_local_spark_docker.ps1`: Windows PowerShell helper for Docker setup.
- `local_delta_smoke_test.py`: verifies local Spark + Delta functionality.

## Usage Notes
- No Bronze/Silver/Gold implementation templates are provided by design.
- Candidates can use notebook-first, script-first, or mixed workflows.
- Core requirement is Spark-first transformation and medallion outputs.

## Local Setup Example
Preferred (isolated runtime, no host Java):

```powershell
Set-Location candidate_pack_databricks
.\starter\databricks\bootstrap_local_spark_docker.ps1
```

Equivalent manual compose flow (Windows/macOS/Linux):

```powershell
Set-Location candidate_pack_databricks\docker
docker compose build spark-local
docker compose run --rm spark-local python starter/databricks/local_delta_smoke_test.py
```

Bash/zsh example:

```bash
cd candidate_pack_databricks/docker
docker compose build spark-local
docker compose run --rm spark-local python starter/databricks/local_delta_smoke_test.py
```

Host install path (if Docker is unavailable):
Prerequisite: Java 17+ must be installed and available on PATH.
If Java is missing on Windows, one option is:

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

```powershell
Set-Location candidate_pack_databricks
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py .\starter\databricks\local_delta_smoke_test.py
```

Use these commands as a baseline and adjust to your preferred workflow.

Handle KEV retrieval inside your ingestion logic rather than relying on a prebuilt helper.

Recommended warehouse path convention for candidate pipeline output: `candidate_pack_databricks/output/warehouse`.

## Generic Table I/O Pattern (Local Spark + Delta)
Use this pattern for local execution (Docker or host), where Spark session setup differs from Databricks notebooks.

```python
from pathlib import Path
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

warehouse_dir = str(Path("output/warehouse").resolve())

builder = (
	SparkSession.builder.appName("candidate_pipeline")
	.master("local[*]")
	.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
	.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
	.config("spark.sql.warehouse.dir", warehouse_dir)
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sql("CREATE DATABASE IF NOT EXISTS candidate_demo")

# Read from a managed Delta table.
df_in = spark.table("candidate_demo.<table_name>")

# Write to a managed Delta table.
df_in.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(
	"candidate_demo.<output_table_name>"
)

spark.stop()
```

Run your script in Docker with:

```powershell
Set-Location candidate_pack_databricks\docker
docker compose run --rm spark-local python starter/databricks/<your_script>.py
```

The managed table files will be written under your configured warehouse path.

Provide your own validation evidence showing Bronze/Silver/Gold outputs are non-empty and reproducible.
