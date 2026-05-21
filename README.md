# model-wnba
dbt data mart that enables comprehensive WNBA artifacts.

# Stack

Python 3.11.15 used. Compatible with dbt-core and dbt-duckdb.

`dbt-core` - 1.11.9
`duckdb` - 1.10.1

[DuckDB used as an embedded warehouse.](https://docs.getdbt.com/docs/local/connect-data-platform/duckdb-setup?version=1.12)

# Raw Ingested Data

Data ingested from ESPN's API layer. Python scripts used to handle ingestion. 