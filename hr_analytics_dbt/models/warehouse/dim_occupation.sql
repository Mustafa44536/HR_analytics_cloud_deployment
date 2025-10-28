select
  row_number() over(order by occupation_name) as id,
  occupation_name as name
from (select distinct occupation_name from {{ ref('stg_job_ads') }}) t
