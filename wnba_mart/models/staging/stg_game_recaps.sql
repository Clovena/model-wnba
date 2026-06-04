with recap_fields as (
  select
  distinct
  game_id, 
  notes[1] as notes_json,
  headlines[1] as headlines_json
  from {{ source('raw', 'competitions') }}
),
final as (
  select
  distinct
  game_id,
  upper(json_value(notes_json, '$.headline')) as game_headline,
  upper(json_value(headlines_json, '$.description')) as game_recap
  from recap_fields
)
select * from final