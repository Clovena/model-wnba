with raw_links as (
  select
  game_id,
  rel[1] as link_type,
  href
  from {{ source('raw', 'game_links') }}
),
final as (
  select
  game_id,
  {{game_link_metrics('link_type')}}
  from raw_links
  group by game_id
)
select * from final