select
  cast(job_id as varchar)                            as job_id,
  coalesce(title, '')                                as title,
  coalesce(city, 'Unknown')                          as city,
  coalesce(occupation_name, 'Unknown')               as occupation_name,
  coalesce(employment_type__label, 'Unknown')        as employment_type,
  cast(published_at as timestamp)                    as published_at,
  coalesce(source_group, '')                         as source_group
from raw.job_ads
