# Data Analytics, BI Reporting & Data Export SOP
Doc Code: DOC-SOP-05 | Type: SOP | Version: 2.0
Department: DATA_AI | Organization: ApexNova Global Technologies

## Section 5.1: BI Query Optimization & Resource Caps
All analytical queries against BigQuery and PostgreSQL warehouses must include partition filters. Ad-hoc queries scanning over 500GB of telemetry require Data Engineering approval.

## Section 5.2: Strict Ban on Local Unencrypted Data Dumps
Downloading unencrypted raw customer datasets or CSV files to local desktop or laptop drives is strictly prohibited. Analysis must occur within secure cloud analytics notebooks.

## Section 5.3: Mandatory Data Masking in BI Dashboards
Credit card numbers, bank routing codes, tax identifiers, and passwords must be irreversibly hashed or masked (e.g. ****-****-1234) before rendering on executive BI dashboards.

## Section 5.4: Third-Party Data Sharing Sign-off
Sharing any analytical data extracts with third-party vendors requires formal sign-off from the Data Governance Board and Legal.

