import os
from typing import List, Dict, Any, Iterable
import dlt
from .jobtech_client import fetch_job_ads


@dlt.resource(name="job_ads", write_disposition="replace")
def job_ads_res(params: Dict[str, Any], occupation_fields: List[str]) -> Iterable[Dict[str, Any]]:
    """
    DLT-resource som hämtar och normaliserar annonser från JobTech.
    - params: basparametrar till /search (ex: {"limit": 100})
    - occupation_fields: lista av taxonomy-ID för 'occupation-field'
    """
    for row in fetch_job_ads(params, occupation_fields):
        # row innehåller redan normaliserade fält som våra dbt-modeller förväntar sig
        yield row


def run() -> None:
    """
    Kör dlt-pipen och laddar till DuckDB (credentials via env).
    OBS: Vi använder env-variabeln DESTINATION__DUCKDB__CREDENTIALS
         för att peka ut filen, t.ex. 'data/hr_warehouse.duckdb'.
    """
    # Läs occupation-fields från .env (eller fall tillbaka till tre standard-ID:n)
    occ_env = os.getenv("JOB_GROUPS", "")
    if occ_env.strip():
        occupation_fields = [x.strip() for x in occ_env.split(",") if x.strip()]
    else:
        # Samma tre som i din tidigare Snowflake-kod
        occupation_fields = ["X82t_awd_Qyc", "NYW6_mP6_vwf", "RPTn_bxG_ExZ"]

    # Basparametrar till JobTech /search (lägg till filter här om du vill)
    params: Dict[str, Any] = {"limit": 100}

    # Skapa pipeline – destination sätts via env (DESTINATION__DUCKDB__CREDENTIALS)
    pipe = dlt.pipeline(
        pipeline_name="jobsearch_duckdb",
        destination="duckdb",
        dataset_name="raw",
        pipelines_dir=".dlt",
    )

    # Kör laddningen till tabellen raw.job_ads
    load_info = pipe.run(
        job_ads_res(params=params, occupation_fields=occupation_fields),
        table_name="job_ads",
    )
    print(load_info)


if __name__ == "__main__":
    run()
