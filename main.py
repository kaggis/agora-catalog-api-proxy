from fastapi import FastAPI, Query
from typing import Optional
import httpx
import os
import toml
from dotenv import load_dotenv
import asyncio

load_dotenv()

AGORA_CATALOG_API = os.getenv("AGORA_CATALOG_API")


def get_version():
    try:
        with open("pyproject.toml", "r") as f:
            pyproject = toml.load(f)
            return pyproject["project"]["version"]
    except Exception as e:
        print(f"Error reading version: {e}")
        return "unknown"


VERSION = get_version()

app = FastAPI(
    title="Service catalog API Proxy Service",
    description="A lightweight api proxy that transforms Service Catalog's API responses",
    version=VERSION,
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Service Catalog API",
        "status": "running",
        "available_endpoints": {
            "/health": "Health check",
            "/services": "Get information on services",
            "/docs": "API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation (ReDoc)",
        },
        "version": VERSION,
    }


@app.get("/health")
async def health():
    return {
        "message": "Service catalog API is running",
        "status": "running",
        "version": VERSION,
    }


@app.get("/services")
async def services(
    offset: Optional[int] = Query(0, alias="from"),
    limit: Optional[int] = Query(10, alias="quantity")
):

    if not AGORA_CATALOG_API:
        return {"error": "AGORA_CATALOG_API env variable not configured"}

    async with httpx.AsyncClient() as client:
        (
            domains_response,
            categories_response,
            order_types_response,
            target_users_response,
            trls_response,
            access_response,
            resources_response,
        ) = await asyncio.gather(
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/domains/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/categories/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/order-types/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/target-users/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/trls/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/access-modes/"),
            client.get(f"{AGORA_CATALOG_API}/api/v2/public/resources/?offset={offset}&limit={limit}"),
        )

    domains = {dom["id"]: dom["eosc_id"] for dom in domains_response.json()}
    categories = {cat["id"]: cat["eosc_id"] for cat in categories_response.json()}
    order_types = {
        order["id"]: order["eosc_id"] for order in order_types_response.json()
    }
    target_users = {usr["id"]: usr["eosc_id"] for usr in target_users_response.json()}
    trls = {trl["id"]: trl["eosc_id"] for trl in trls_response.json()}
    access = {acc["id"]: acc["eosc_id"] for acc in access_response.json()}

    resp = resources_response.json()
    data = resp["results"]
    count = resp["count"]
    start = offset
    end = offset + (len(data)-1)

    data_mod = [
        {
            "id": item.get("id"),
            "service": {
                "id": item.get("id"),
                "name": item.get("erp_bai_name"),
                "abbreviation": item.get("erp_bai_abbreviation"),
                "webpage": item.get("erp_bai_webpage"),
                "description": item.get("erp_mri_description"),
                "tagline": item.get("erp_mri_tagline"),
                "logo": item.get("erp_mri_logo"),
                "tags": [tag.strip() for tag in item.get("erp_cli_tags").split(",")],
                "languageAvailabilities": [lang.strip() for lang in item.get("erp_gla_language").split(",")],
                "scientificDomains": [
                    {"scientificDomain": domains[dom_item["id"]]}
                    for dom_item in item.get("erp_cli_scientific_domain")
                ],
                "categories": [
                    {"category": categories[cat_item["id"]]}
                    for cat_item in item.get("erp_cli_category")
                ],
                "targetUsers": [
                    target_users[usr_item["id"]]
                    for usr_item in item.get("erp_cli_target_users")
                ],
                "orderType": (
                    order_types[item.get("erp_aoi_order_type")["id"]]
                    if item.get("erp_aoi_order_type")
                    else None
                ),
                "trl": (
                    trls[item.get("erp_mti_technology_readiness_level")["id"]]
                    if item.get("erp_mti_technology_readiness_level")
                    else None
                ),
                "accessModes": [
                    access[acc_item["id"]]
                    for acc_item in item.get("erp_cli_access_mode")
                ],
                "securityContactEmail": item.get("erp_coi_security_contact_email"),
                "helpdeskEmail": item.get("erp_coi_helpdesk_email"),
                "userManual": item.get("erp_mgi_user_manual"),
                "termsOfUse": item.get("erp_mgi_terms_of_use"),
                "privacyPolicy": item.get("erp_mgi_privacy_policy"),
                "accessPolicy": item.get("erp_mgi_access_policy")
            },
        }
        for item in data
    ]

    # Transform the response format
    return {"total": count, "from": start, "to": end, "results": data_mod}
