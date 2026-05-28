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