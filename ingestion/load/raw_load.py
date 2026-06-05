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
broadcasts_df = []
competitors_df = []

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
  links_list = []
  for _, row in df.iterrows():
      game_links = pd.json_normalize(row['links'])
      game_links['game_id'] = row['id']
      links_list.append(game_links)
  links_temp = pd.concat(links_list, ignore_index=True)
  # Normalize competitions array
  competitions_list = []
  for _, row in df.iterrows():
      comp = pd.json_normalize(row['competitions'][0])
      comp = comp.rename(columns={'id': 'game_id'})
      competitions_list.append(comp)
  competitions_temp = pd.concat(competitions_list, ignore_index=True)
  ## Sub-arrays from competitions
  broadcasts_list = []
  competitors_list = []
  for _, row in competitions_temp.iterrows():
      game_id = row['game_id']
      comps = pd.json_normalize(row['competitors'])
      comps['game_id'] = game_id
      competitors_list.append(comps)
      for broadcast in row['broadcasts']:
          broadcast['game_id'] = game_id
          broadcasts_list.append(broadcast)
  broadcasts_temp = pd.DataFrame(broadcasts_list)
  competitors_temp = pd.concat(competitors_list, ignore_index=True)
  competitors_temp = competitors_temp.drop(
    columns=['broadcasts', 'competitors','linescores', 'statistics', 'leaders', 'records', 'team.links'],
    errors='ignore'
  )
  # Append dfs
  metadata_df.append(metadata_temp)
  links_df.append(links_temp)
  competitions_df.append(competitions_temp)
  broadcasts_df.append(broadcasts_temp)
  competitors_df.append(competitors_temp)

# Load to DuckDB
metadata_df = pd.concat(metadata_df, ignore_index = True)
links_df = pd.concat(links_df, ignore_index = True)
competitions_df = pd.concat(competitions_df, ignore_index = True)
broadcasts_df = pd.concat(broadcasts_df, ignore_index = True)
competitors_df = pd.concat(competitors_df, ignore_index = True)

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.register('metadata_df', metadata_df)
con.register('links_df', links_df)
con.register('competitions_df', competitions_df)
con.register('broadcasts_df', broadcasts_df)
con.register('competitors_df', competitors_df)

con.execute("CREATE OR REPLACE TABLE raw.games AS SELECT * FROM metadata_df")
con.execute("CREATE OR REPLACE TABLE raw.game_links AS SELECT * FROM links_df")
con.execute("CREATE OR REPLACE TABLE raw.competitions AS SELECT * FROM competitions_df")
con.execute("CREATE OR REPLACE TABLE raw.broadcasts AS SELECT * FROM broadcasts_df")
con.execute("CREATE OR REPLACE TABLE raw.competitors AS SELECT * FROM competitors_df")
