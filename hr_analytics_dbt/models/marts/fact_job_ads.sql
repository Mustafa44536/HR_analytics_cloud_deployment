with s as (select * from {{ ref('stg_job_ads') }}),
c as (select * from {{ ref('dim_city') }}),
o as (select * from {{ ref('dim_occupation') }}),
e as (select * from {{ ref('dim_employment_type') }})
select
  s.job_id,
  s.title,
  c.id as city_id,
  o.id as occupation_id,
  e.id as employment_type_id,
  cast(s.published_at as timestamp) as published_at,
  s.source_group
from s
left join c on s.city = c.name
left join o on s.occupation_name = o.name
left join e on s.employment_type = e.name
