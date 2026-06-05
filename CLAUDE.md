# CLAUDE.md

Operational reference for Claude Code sessions in this repo. Reflects the *current* state of the codebase — update as decisions change.

---

## What this project is

A **dbt portfolio project**: a WNBA data mart sourced from ESPN's hidden API, designed to demonstrate analytics engineering competency (dbt Core, DuckDB, Python ingestion). Target audience for the *data* is analytical storytellers (Jon Bois / The Athletic style). Target audience for the *project* is hiring managers and freelance prospects evaluating dbt skills.

Secondary goal: build Python fluency alongside the user's existing R/SQL background — which is why ingestion is Python rather than something shell-glued.

---

## Stack

| Layer | Tool |
|---|---|
| Source | ESPN hidden API (no auth, undocumented) |
| Extract / load | Python 3.11 (`requests`, `pandas`, `duckdb`) |
| Warehouse | DuckDB (single file: `ingestion/load/wnba.duckdb`) |
| Transform | dbt Core + `dbt-duckdb` adapter |
| Venv | `dbt-env/` at repo root (gitignored) |

`dbt-core` 1.11.9, `duckdb` 1.10.1. Python 3.11.x via Homebrew on Apple Silicon.

---

## How to run

**Always activate the venv first:**
```bash
source /Users/zjricker/repos/model-wnba/dbt-env/bin/activate
```

**Ingestion** — run from repo root with `-m`. Running the file directly breaks imports.
```bash
cd /Users/zjricker/repos/model-wnba
python -m ingestion.load.raw_load
```

**dbt** — run from the dbt project dir.
```bash
cd /Users/zjricker/repos/model-wnba/wnba_mart
dbt run
dbt run --select stg_game_names    # single model
dbt debug                          # verify connection
```

**`profiles.yml` lives at `~/.dbt/profiles.yml`** (not in repo). Uses absolute path to the DuckDB file. DuckDB has no catalog layer — don't add `database:` anywhere, and don't reference `wnba.raw.games`, just `raw.games`.

---

## Architecture

```
ESPN API
  → Python (requests, pandas)       # HTTP + JSON flattening
    → DuckDB raw.* tables           # landing zone — Python owns this
      → dbt main_staging.stg_*      # rename, cast, simple booleans
        → dbt main_marts.*          # joins, aggregations, business logic
```

**Schema ownership is strict:** dbt reads `raw.*` but never writes to it. dbt writes only to `main_staging` and `main_marts` (dbt-duckdb prepends the target name — `main_` — to declared schemas; this is expected behavior).

**Layer discipline:**
- **Raw**: preserve source shape. Structural flattening OK; no business logic.
- **Staging**: rename, cast, simple boolean flags. No joins, no aggregations.
- **Marts**: analytical grain, joins, aggregations, derived metrics. Parse `series.summary`, derive averages, etc.

---

## Repo layout

```
model-wnba/
├─ ingestion/
│  ├─ extract/espn_client.py     # HTTP wrapper with retry/backoff
│  ├─ load/raw_load.py           # main ingestion pipeline
│  └─ load/wnba.duckdb           # local DuckDB file (gitignored)
├─ wnba_mart/                    # dbt project
│  ├─ dbt_project.yml
│  ├─ models/staging/            # stg_* models + _sources.yml + schema.yml
│  ├─ models/marts/              # not yet built
│  └─ macros/                    # game_link_metrics.sql lives here
├─ CLAUDE.md                     # this file
├─ TASKS.md                      # session-level scratchpad / questions
└─ README.md
```

---

## ESPN API reference

**Base:** `https://site.api.espn.com/apis/site/v2/sports/basketball/wnba` (used by `espn_client.get`)
**Core:** `https://sports.core.api.espn.com/v2/sports/basketball/leagues/wnba` (used by `get_core` — reserved for deeper data like PBP)

**Key endpoints:**
- `/scoreboard?dates=YYYYMMDD` — games for that date. Passing any in-season date (e.g. `20260501`) returns the full season calendar under `leagues[0].calendar`, which is how `raw_load.py` derives the date list without brute-forcing.
- `/summary?event={game_id}` — full game package (boxscore, PBP). **Not yet wired up.**
- `/teams`, `/teams/{team_id}` — team identity.

**Rate limiting:** none documented. Client uses `time.sleep(1)` between requests and `time.sleep(30)` on 429. Endpoints can change without notice.

**UID format:** `s:40~l:59~e:{event_id}` — sport 40 (basketball), league 59 (WNBA). Numeric `id` is sufficient as a primary key; `uid` is ESPN's global composite key.

---

## DuckDB raw schema — current state

Loaded by [ingestion/load/raw_load.py](ingestion/load/raw_load.py):

| Table | Grain |
|---|---|
| `raw.games` | one row per game (id, uid, date, name, shortName, season fields, status fields) |
| `raw.game_links` | one row per link per game |
| `raw.competitions` | one row per competition per game |
| `raw.broadcasts` | one row per broadcast market per game |
| `raw.competitors` | one row per team per game |

**Currently dropped** from `raw.competitors` before load (see [raw_load.py:79-82](ingestion/load/raw_load.py#L79-L82)) and *not yet landed anywhere*: `linescores`, `statistics`, `leaders`, `records`, `team.links`, plus nested `broadcasts`/`competitors`. These need to be extracted into their own `raw.*` tables before that drop if we want them downstream.

**Seasons loaded:** 2020–present (`seasons` list in [raw_load.py:10-18](ingestion/load/raw_load.py#L10-L18)). 2019 was discussed in early planning but is not currently in the load.

**Incremental logic:** the loader queries existing `raw.games` for distinct dates, fetches each season's calendar, and only pulls dates that are past *and* not already loaded. Each table is then `CREATE OR REPLACE`'d from the accumulated DataFrame — so it's incremental in *fetching* but full-replace in *writing*. Fine at current scale.

**Known limitation:** date is the dedup key. ESPN historical corrections won't be re-pulled. Documented tradeoff.

---

## Staging models — current state

Live in [wnba_mart/models/staging/](wnba_mart/models/staging/):

- `stg_game_names.sql` — game identity / naming fields
- `stg_game_links.sql` — link rows pivoted to columns via the `game_link_metrics` macro
- `stg_game_metadata.sql` — currently in progress (untracked in git as of this writing)
- `stg_game_recaps.sql` — recap text fields
- `stg_venues.sql` — venue dimension (split out from competitions)

Originally there was a single `stg_games.sql`; it was split as the model grew. See recent git history for the split rationale.

**Sources declared in `_sources.yml`:** `games`, `game_links`, `competitions`. `broadcasts` and `competitors` are loaded into DuckDB but not yet declared as sources.

**`schema.yml`** still references `stg_games` (the now-removed pre-split model) — stale and needs updating when the new models stabilize.

**Active macro:** `game_link_metrics(field)` in [wnba_mart/macros/game_link_metrics.sql](wnba_mart/macros/game_link_metrics.sql) — pivots link-type rows into columns using `MAX(CASE WHEN ...)` grouped by `game_id`.

---

## Naming conventions

**Booleans:** `is_` for state (`is_playoff`, `is_neutral_site`), `has_` for occurrence (`has_overtime`).

**Season/game type:**
- `season_type` — `PRESEASON` | `REGULAR SEASON` | `POSTSEASON`
- `game_stage` — `STANDARD` | `FIRST ROUND` | `SEMIFINALS` | `FINALS` | `COMMISSIONER'S CUP` | `ALL STAR`
- `is_playoff` — convenience: `game_stage IN ('FIRST ROUND','SEMIFINALS','FINALS')`

**Broadcasts:** `national_broadcast`, `home_broadcast`, `away_broadcast`.

**Link columns:** `{type}_link` — `summary_link`, `boxscore_link`, `pbp_link`, `recap_link`, `highlights_link`.

**Playoff series:** `series_summary` stays raw in staging; parse into `series_winner` / `series_wins` / `series_losses` / `series_is_clinching` in marts.

**ESPN game-type code map:**
```
type.id 1  → STANDARD
type.id 4  → ALL STAR GAME
type.id 14 → FIRST ROUND
type.id 16 → SEMIFINALS
type.id 17 → FINALS
type.id 39 → COMMISSIONER'S CUP
```

---

## Data quality issues to know

1. **International exhibitions** in early seasons — e.g. `team.id = 21` ("CHINA"), Toyota Antelopes (`team.id = 130927`). Filter in staging with a documented reason; don't silently drop in Python.
2. **`active` flag is current-state**, not game-time. A player who appeared in a 2020 game may show `active: false` today. Don't use it to infer historical roster status.
3. **`avg*` stats are always `0.0`** — ESPN populates them progressively. Drop from staging; derive averages in marts.
4. **`highlights` link often absent** — `MAX(CASE WHEN ...)` handles this with a natural null.
5. **`recap` link absent for older / preseason games.**
6. **`series.summary` only present for playoff games** — null for regular and preseason.
7. **Period ≥5 in `linescores` = overtime** — cross-check for `has_overtime` once linescores are landed.
8. **`short_name` inconsistent** — preseason uses `VS`, regular season uses `@`. ESPN source issue. Don't normalize in staging; document.
9. **PBP coverage is patchy** across seasons — document gaps explicitly when Phase 2 lands.

---

## Gotchas (things that will bite you)

1. **Run ingestion with `python -m ingestion.load.raw_load`** from repo root. Direct file execution breaks `from ingestion.extract.espn_client import get`.
2. **Never `touch` the `.duckdb` file.** An empty file is not a valid DuckDB database — let `duckdb.connect()` create it.
3. **`profiles.yml` uses absolute paths.** dbt has no stable working-directory assumption.
4. **No `database:` field in `_sources.yml`.** DuckDB has no catalog layer.
5. **Jinja string literals need quotes inside SQL** — `'{{ metric }}'` not `{{ metric }}` when passing into `CASE WHEN ... = '...'`.
6. **Column aliases aren't available in the same `SELECT`** — use a CTE if you need to reference a derived column in a `CASE WHEN` or `WHERE`.
7. **`pd.concat` after the loop**, not inside it — repeated in-loop concat is O(n²).
8. **`df['id'].iloc[0]` to extract a scalar** — `df['id']` is a Series; assigning a Series to a new column triggers index alignment and silently produces NaNs.
9. **`errors='ignore'` when dropping** ESPN columns — schemas vary across game types; defensive drops avoid `KeyError` on edge cases.
10. **Scoreboard returns future games** — the `<= date.today()` filter excludes them. Loading future dates pollutes the dataset with scheduled-but-not-played records.
11. **dbt-duckdb prepends `main_` to schema names.** Declared `staging` resolves to `main_staging`. Override with a `generate_schema_name` macro if/when clean names are wanted — deferred.

---

## SCD / historical tracking note

dbt snapshots capture changes *going forward* — they cannot retroactively reconstruct history. For team relocations (Tulsa Shock → Dallas Wings, San Antonio Stars → Las Vegas Aces), mid-season trades, and expansion teams (Golden State Valkyries in 2025), a manually curated seed file is the realistic path. Snapshots are appropriate for changes observed *during* the project's lifetime.

---

## Conventions for working in this repo

- **README is portfolio-facing.** Anything that goes there should serve the "show dbt competency" thesis. Internal reference / gotchas go here in CLAUDE.md, not the README.
- **TASKS.md is a scratchpad** for the current session's open questions and todos. Not durable across sessions; safe to overwrite.
- **Don't add features the task doesn't require.** This is a portfolio project — clarity and correctness beat scope. A staging model doesn't need 12 columns when the source has 6 useful ones.
- **Update this file when decisions change** — schema choices, naming changes, new tables landed, new gotchas discovered.
