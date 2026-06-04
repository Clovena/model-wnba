with final as (
  select 
  id as game_id,
  year,

  "type" as season_type_cd,
  upper(slug) as season_type_desc,

  upper("name") as long_name,
  upper(shortName) as short_name

  from {{ source('raw', 'games') }}
)
select * from final