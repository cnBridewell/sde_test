# CPE to CVE Applicability Bridge

This folder provides a deterministic bridge dataset to make CPE-to-CVE linkage feasible within take-home scope.

## File
- `cve_cpe_applicability.csv`

## Guarantee
Every row is constructed to match:
- a real `cve_id` from the live CISA KEV feed used at generation time, and
- a real `cpe23_uri` present in `data/internal_synthetic/asset_software.csv`.

## Columns
- `cve_id`
- `cpe23_uri`
- `is_vulnerable`
- `match_confidence`
- `match_method`
- `source`
- `notes`

## Notes
- This bridge is provided for task feasibility and deterministic linkage.
- The bridge includes multiple KEV CVEs for each internal CPE where available, so exposure analysis has broader vulnerability diversity.
- Candidates may still add optional enrichment (EPSS, NVD detail) if they want to improve scoring logic.
