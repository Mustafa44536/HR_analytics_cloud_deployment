import os
import json
import requests
from typing import Dict, Iterable, List, Any

BASE_URL = "https://jobsearch.api.jobtechdev.se"
SEARCH_URL = f"{BASE_URL}/search"


def _headers() -> Dict[str, str]:
    """Eventuell API-nyckel (om/när det behövs)."""
    h = {"accept": "application/json"}
    api_key = os.getenv("JOBTECH_API_KEY")
    if api_key:
        h["Authorization"] = f"Bearer {api_key}"
    return h


def _get_ads(params: Dict[str, Any]) -> Dict[str, Any]:
    """Gör ett anrop mot /search och returnerar JSON."""
    r = requests.get(SEARCH_URL, headers=_headers(), params=params, timeout=30)
    r.raise_for_status()
    return json.loads(r.content.decode("utf-8"))


def fetch_job_ads(
    params_base: Dict[str, Any],
    occupation_fields: List[str],
) -> Iterable[Dict[str, Any]]:
    """
    Paginera över /search per occupation-field och yielda normaliserade rader.
    Vi mappar fälten till våra dbt-staging-fält.
    """
    limit = int(params_base.get("limit", 100))

    for occ_field in occupation_fields:
        offset = 0
        while True:
            params = {
                **params_base,
                "occupation-field": occ_field,  # taxonomy-id
                "offset": offset,
                "limit": limit,
            }
            try:
                data = _get_ads(params)
            except requests.exceptions.HTTPError:
                # Slut på giltiga träffar eller fel → avbryt den här occ_field
                break

            hits = data.get("hits", [])
            if not hits:
                break

            for ad in hits:
                # --- Normalisering till våra dbt-fält ---
                # OBS: Fältnamn kan skilja lite i API:t – justera vid behov
                job_id = ad.get("id")
                title = ad.get("headline") or ad.get("title") or ""
                city = (ad.get("workplace_address") or {}).get("municipality") or ""
                occupation_name = None
                occ = ad.get("occupation") or {}
                if isinstance(occ, dict):
                    occupation_name = occ.get("label") or occ.get("name")
                employment_type = ad.get("employment_type") or ad.get("employment_type_label") or ""
                published_at = ad.get("publication_date") or ad.get("published")  # kan vara ISO- eller epoch

                yield {
                    "job_id": job_id,
                    "title": title,
                    "city": city or "Unknown",
                    "occupation_name": (occupation_name or "Unknown"),
                    "employment_type": (employment_type or "Unknown"),
                    "published_at": published_at,
                    "source_group": occ_field,  # spara vilken occupation-field som använts
                }

            offset += limit
