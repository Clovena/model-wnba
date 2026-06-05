--- TODO: broadcasts[], competitiors[], geoBroadcasts[]

select
game_id,

"date" as timestamp,
substr("date", 1, 10)::date as "date",

attendance,
neutralSite as is_neutral_site,
conferenceCompetition as is_conference_competition,

upper(broadcast) as broadcast,

"type.id" as game_format_cd,
upper("type.abbreviation") as game_format_desc,
case
  when "type.id" = 1  then 'REGULAR SEASON'
  when "type.id" = 14 then 'FIRST ROUND'
  when "type.id" = 16 then 'SEMIFINALS'
  when "type.id" = 17 then 'FINALS'
  when "type.id" = 39 then 'COMMISSIONER''S CUP'
  when "type.id" = 4  then 'ALL STAR GAME'
  else 'UNKNOWN' end
  as game_format_detail,
case
  when lower("series.type") = 'playoff' then true
  else false end
as is_playoff,
upper("series.summary") as series_summary,
"series.completed" as is_elimination_game,

"status.period" as periods_played,
case
  when lower("status.type.detail") = 'final' then false
  when lower("status.type.detail") like 'final%' then true
  else null end
  as has_overtime,
"status.period"::integer - "format.regulation.periods"::integer as overtime_periods

from {{ source('raw', 'competitions') }}