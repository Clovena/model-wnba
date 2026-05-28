import duckdb
import pandas as pd
from datetime import date
from ingestion.extract.espn_client import get

# Settings and connections
con = duckdb.connect('ingestion/load/wnba.duckdb')

# Compile valid dates for loading
seasons = [
  '20200501', 
  '20210501', 
  '20220501', 
  '20230501', 
  '20240501', 
  '20250501',
  '20260501'
  ]

try:
  loaded_dates = {row[0] for row in con.execute("""
    SELECT DISTINCT STRFTIME(CAST(date AS DATE), '%Y%m%d')
    FROM raw.games
  """).fetchall()}
except:
  loaded_dates = set()

valid_dates = []
for s in seasons:
  calendar = pd.json_normalize(get('scoreboard', params={'dates': s})['leagues'])['calendar'][0]
  valid_dates.extend([c[:10].replace('-', '') for c in calendar
                     if c[:10].replace('-', '') <= date.today().strftime('%Y%m%d')
                     and c[:10].replace('-', '') not in loaded_dates])

# Init dfs and loop through valid dates
metadata_df = []
links_df = []
competitions_df = []

for d in valid_dates:
  print(d)
  raw_data = get('scoreboard', params={'dates': d})
  events = raw_data['events']
  df = pd.DataFrame(events)

  # Normalize simple metadata
  id_df = df[['id', 'uid', 'date', 'name', 'shortName']]
  season_df = pd.json_normalize(df.season)
  status_df = pd.json_normalize(df.status)
  metadata_temp = id_df.join(season_df).join(status_df)

  # Normalize links array
  links_temp = pd.json_normalize(df.links.iloc[0])
  links_temp['game_id'] = df['id'].iloc[0]

  # Normalize competitions array
  competitions_temp = pd.json_normalize(df.competitions.iloc[0]).rename(columns={'id': 'game_id'})

  metadata_df.append(metadata_temp)
  links_df.append(links_temp)
  competitions_df.append(competitions_temp)

# Load to DuckDB
metadata_df = pd.concat(metadata_df, ignore_index=True)
links_df = pd.concat(links_df, ignore_index=True)
competitions_df = pd.concat(competitions_df, ignore_index=True)

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.register('metadata_df', metadata_df)
con.register('links_df', links_df)
con.register('competitions_df', competitions_df)

con.execute("CREATE OR REPLACE TABLE raw.games AS SELECT * FROM metadata_df")
con.execute("CREATE OR REPLACE TABLE raw.game_links AS SELECT * FROM links_df")
con.execute("CREATE OR REPLACE TABLE raw.competitions AS SELECT * FROM competitions_df")
