# Agora Catalog Api Proxy
API proxy to translate catalog data to different schema

## Prerequisites

- Python 3.9+
- Poetry (recommended) or pip

## Installation

### Option 1: Using Poetry 

```bash
# Clone the repository
git clone https://github.com/argoeu/argo-een
cd argo-een

# Install dependencies
poetry install

# Create .env file
cp .env.example .env
# Edit .env and set your ARGO_EEN_SOURCE_API
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/argoeu/argo-een
cd argo-een

# Create virtual environment
python -m venv venv
source venv/bin/activate 

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and set your  ARGO_EEN_SOURCE_API
```

## Configuration

Create a `.env` file in the project root:

```env
AGORA_CATALOG_API=https://api.example.com
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AGORA_CATALOG_API` | The external API endpoint to proxy results from | Yes |

## Running the Service

### Development Mode

#### With Poetry:

```bash
poetry run uvicorn main:app --reload
```

#### With pip (after activating venv):

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

For production, run without `--reload` and specify host/port:

```bash
# With Poetry
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With pip
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint |
| `/services` | GET | Get the services data in the new format |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation (ReDoc) |

### Example Request

```bash
curl http://localhost:8000/services
```

### Example Response

```json
{
    "total": 3,
    "from": 0,
    "to": 2,
    "results": [
        {
            "id": "03bc487d-6d3b-4988-81cc-60524522b3f8",
            "service": 
            {
                "id": "03bc487d-6d3b-4988-81cc-60524522b3f8",
                "name": "SERVICE_A",
                "abbreviation": "sa",
                "website": "service-a.example.com",
                "tagline":"this is service a",
                "description":"description of service a",
                "logo":"http://service-a.example.com/img/logo.png",
                "tags": ["tag1","tag2"],
                "languageAvailabilities": [
                    "en"
                ],
                "scientificDomains": [
                    {
                        "scientificDomain": "scientific_domain-generic"
                    },
                    {
                        "scientificDomain": "scientific_domain-engineering_and_technology"
                    }
                ],
                "categories": [
                    {
                        "category": "category-sharing_and_discovery-data"
                    },
                    {
                        "category": "category-processing_and_analysis-data_analysis"
                    },
                ],
                "targetUsers": [
                    "target_user-research_groups",
                    "target_user-resource_provider_managers",
                    "target_user-research_managers",
                ],
                "orderType": "order_type-order_required",
                "trl": "trl-9",
                "accessModes": [
                    "access_mode-free_conditionally",
                    "access_mode-paid"
                ],
                "securityContactEmail": "security-service-a@example.com",
                "helpdeskEmail": "helpdesk-service-a@example.com",
                "userManual": "https://service-a.example.com/user-manual",
                "termsOfUse": "https://service-a.example.com/terms",
                "privacyPolicy": "https://service-a.example.com/privacy",
                "accessPolicy": "https://service-a.example.com/policy"
            }
        },
        {
            "id": "53d9cb1b-e102-42a5-95b3-be0edf687cf1",
            "service": {
                "id": "53d9cb1b-e102-42a5-95b3-be0edf687cf1",
                "name": "SERVICE_B",
                "abbreviation": "sb",
                "website": "service-b.example.com",
                "tagline":"this is service b",
                "description":"description of service b",
                "logo":"http://service-b.example.com/img/logo.png",
                "tags": ["tag1"],
                "languageAvailabilities": [
                    "en"
                ],
                "scientificDomains": [
                    {
                        "scientificDomain": "scientific_domain-generic"
                    }
                ],
                "categories": [
                    {
                        "category": "category-processing_and_analysis-data_analysis"
                    },
                ],
                "targetUsers": [
                    "target_user-research_managers",
                ],
                "orderType": "order_type-order_required",
                "trl": "trl-9",
                "accessModes": [
                    "access_mode-paid"
                ],
                "securityContactEmail": "security-service-b@example.com",
                "helpdeskEmail": "helpdesk-service-b@example.com",
                "userManual": "https://service-b.example.com/user-manual",
                "termsOfUse": "https://service-b.example.com/terms",
                "privacyPolicy": "https://service-b.example.com/privacy",
                "accessPolicy": "https://service-b.example.com/policy"
            }
           
        },
        {
            "id": "62b10699-9491-4821-bb38-70a03ec5b22d",
            "service": {
                "id": "62b10699-9491-4821-bb38-70a03ec5b22d",
                "name": "SERVICE_C",
                "abbreviation": "sc",
                "website": "service-c.example.com",
                "tagline":"this is service c",
                "description":"description of service c",
                "logo":"http://service-c.example.com/img/logo.png",
                "tags": ["tag3","tag4"],
                "languageAvailabilities": [
                    "en",
                    "fr"
                ],
                "scientificDomains": [
                    {
                        "scientificDomain": "scientific_domain-generic"
                    },
                    {
                        "scientificDomain": "scientific_domain-engineering_and_technology"
                    }
                ],
                "categories": [
                    {
                        "category": "category-sharing_and_discovery-data"
                    }
                ],
                "targetUsers": [
                    "target_user-research_groups",
                    "target_user-research_managers",
                ],
                "orderType": "order_type-order_required",
                "trl": "trl-9",
                "accessModes": [
                    "access_mode-free"
                ],
                "securityContactEmail": "security-service-c@example.com",
                "helpdeskEmail": "helpdesk-service-c@example.com",
                "userManual": "https://service-c.example.com/user-manual",
                "termsOfUse": "https://service-c.example.com/terms",
                "privacyPolicy": "https://service-c.example.com/privacy",
                "accessPolicy": "https://service-c.example.com/policy"
            }
        }
    ]
}
```

### Url params:

| Url param | Type | Description |
|----------|--------|-------------|
| `from` | Integer | Starting index in the result set (0-based) |
| `quantity` | GET | Number of results to fetch (default 10) |

### Examples with range

```bash
curl http://localhost:8000/services?from=1&quantity=2
```