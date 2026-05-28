with metadata as (
  select 
  id as game_id,

  "date" as timestamp,
  substr("date", 1, 10)::date as "date",
  year,

  "type" as game_type_cd,
  upper(slug) as game_type_desc,

  upper("name") as long_name,
  upper(shortName) as short_name,

  "period" as periods_played,
  case
    when "type.altDetail" = 'OT' then TRUE
    else FALSE end
    as has_overtime

  from {{ source('raw', 'games') }}
),
raw_links as (
  select
  game_id,
  rel[1] as link_type,
  href
  from {{ source('raw', 'game_links') }}
),
flattened_links as (
  select
  game_id,
  {{game_link_metrics('link_type')}}
  from raw_links
  group by game_id
),
final as (
  select * from metadata
  inner join flattened_links
    using(game_id)
)
select * from final