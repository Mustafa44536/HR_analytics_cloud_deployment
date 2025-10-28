select
  row_number() over(order by employment_type) as id,
  employment_type as name
from (select distinct employment_type from {{ ref('stg_job_ads') }}) t
