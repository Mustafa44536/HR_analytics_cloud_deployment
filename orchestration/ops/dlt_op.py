from dagster import op
import os, sys, subprocess

@op
def run_dlt():
    """Kör vår dlt-pipeline som fyller raw.job_ads i DuckDB."""
    env = os.environ.copy()
    # Pekar dlt mot rätt DuckDB-fil om DUCKDB_PATH finns
    if "DUCKDB_PATH" in env:
        env["DESTINATION__DUCKDB__CREDENTIALS"] = env["DUCKDB_PATH"]
    subprocess.run([sys.executable, "-m", "dlt_code.pipeline"], check=True, env=env)

