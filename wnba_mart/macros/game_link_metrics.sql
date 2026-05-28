{% macro game_link_metrics(field) %}
  {%- set metric_list = ['summary', 'boxscore', 'highlights', 'pbp', 'recap'] -%}

  {%- for metric in metric_list -%}
    max(case when {{field}} = '{{metric}}' then href end) as {{metric}}_link
    {%- if not loop.last -%} ,
    {%- endif -%}
  {%- endfor -%}
{% endmacro %}