from dagster import job
from .ops.dlt_op import run_dlt
from .ops.dbt_op import run_dbt

@job
def daily_etl_job():
    """Kör dlt → dbt utan att skicka data."""
    run_dlt()
    run_dbt()
