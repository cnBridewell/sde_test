# Synthetic Internal Data

This folder contains the internal source data for the take-home task.

## Files
- `assets.csv`
- `asset_software.csv`

Use the CSV files as the expected source format for this variant.
Treat them as a static snapshot of internal data that would normally be refreshed by a scheduled internal ingestion pipeline.

## Dataset Overview
### `assets`
One row per asset, including:
- `asset_id`, `hostname`
- `business_unit`, `criticality`, `environment`
- `owner_name`, `owner_email`
- `is_internet_facing`

### `asset_software`
One row per software installation record, including:
- `asset_software_id`, `asset_id`
- `vendor`, `product`, `version`
- `cpe`, `install_source`

## Data Quality Characteristics
The dataset intentionally includes realistic data-quality imperfections for validation and testing.
Part of the exercise is identifying and handling these in your pipeline/reporting approach.

## Usage Notes
- Data is synthetic (not production data).
