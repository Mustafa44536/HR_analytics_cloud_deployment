from dagster import op
import os, sys, subprocess

@op
def run_dbt():
    """Kör dbt för att bygga staging/dim/fact i schema 'analytics'."""
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = "hr_analytics_dbt"

    if "DUCKDB_PATH" in env and "DESTINATION__DUCKDB__CREDENTIALS" not in env:
        env["DESTINATION__DUCKDB__CREDENTIALS"] = env["DUCKDB_PATH"]

    subprocess.run([sys.executable, "-m", "dbt", "run", "--project-dir", "hr_analytics_dbt"], check=True, env=env)


