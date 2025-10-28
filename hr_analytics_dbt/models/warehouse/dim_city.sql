select
  row_number() over(order by city) as id,
  city as name
from (select distinct city from {{ ref('stg_job_ads') }}) t
