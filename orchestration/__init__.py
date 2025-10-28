from dagster import Definitions
from .jobs import daily_etl_job
from .schedules import daily_schedule

defs = Definitions(
    jobs=[daily_etl_job],
    schedules=[daily_schedule],
)
