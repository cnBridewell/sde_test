"""Validate local Spark + Delta setup with a minimal write/read smoke test."""

from __future__ import annotations

import json
import importlib
import os
from pathlib import Path


def build_spark():
    spark_session = importlib.import_module("pyspark.sql").SparkSession
    configure = importlib.import_module("delta").configure_spark_with_delta_pip
    pack_root = Path(__file__).resolve().parents[2]
    warehouse_dir = os.getenv("DB_WAREHOUSE_DIR", str(pack_root / "output" / "warehouse"))
    builder = (
        spark_session.builder.appName("delta_smoke_test")
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.warehouse.dir", warehouse_dir)
    )
    return configure(builder).getOrCreate()


def main() -> None:
    spark = build_spark()
    out_dir = Path("output/local_smoke")
    out_dir.mkdir(parents=True, exist_ok=True)

    delta_path = str(out_dir / "delta_table")
    df = spark.createDataFrame(
        [
            ("ok", 1),
            ("ok", 2),
        ],
        ["status", "value"],
    )
    df.write.format("delta").mode("overwrite").save(delta_path)

    reloaded = spark.read.format("delta").load(delta_path)
    row_count = reloaded.count()

    result = {
        "delta_path": delta_path,
        "warehouse_path": spark.conf.get("spark.sql.warehouse.dir"),
        "row_count": row_count,
        "status": "pass" if row_count == 2 else "fail",
    }
    summary_path = out_dir / "delta_smoke_test_result.json"
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    print(f"Wrote {summary_path}")
    spark.stop()


if __name__ == "__main__":
    main()
