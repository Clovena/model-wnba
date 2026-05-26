# model-wnba
dbt data mart that enables comprehensive WNBA artifacts.

# Stack

Python 3.11.15 used. Compatible with dbt-core and dbt-duckdb.

`dbt-core` - 1.11.9
`duckdb` - 1.10.1

[DuckDB used as an embedded warehouse.](https://docs.getdbt.com/docs/local/connect-data-platform/duckdb-setup?version=1.12)

# Project Directories

```
model-wnba/
├─ ingestion/
│  ├─ __init__.py
│  ├─ extract/
│  │  ├─ __init__.py
│  │  ├─ espn_client.py
│  ├─ load/
│  │  ├─ __init__.py
│  │  ├─ raw_load.py
│  ├─ transform/
├─ wnba_mart/
│  ├─ analyses/
│  ├─ macros/
│  ├─ models/
│  ├─ seeds/
│  ├─ snapshots/
│  ├─ tests/
├─ .gitignore
├─ README.md
```

# Raw Ingested Data

Data ingested from ESPN's API layer. Python scripts used to handle ingestion. 

# References

- [ESPN API documentation](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b#wnba)