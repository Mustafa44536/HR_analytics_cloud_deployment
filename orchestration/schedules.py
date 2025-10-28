from dagster import ScheduleDefinition
from .jobs import daily_etl_job

daily_schedule = ScheduleDefinition(
    job=daily_etl_job,
    cron_schedule="0 6 * * *",  # 06:00 varje dag
    execution_timezone="Europe/Stockholm",
)

