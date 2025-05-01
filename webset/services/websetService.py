import os

from dotenv import load_dotenv
from exa_py import Exa
from exa_py.websets.types import CreateWebsetParameters, CreateEnrichmentParameters


load_dotenv()
exa = Exa(os.getenv('EXA_API_KEY'))

#Response of creating a webset
"""
{
  "id": "<string>",
  "object": "webset",
  "status": "idle",
  "externalId": "<string>",
  "searches": [
    {
      "id": "<string>",
      "object": "webset_search",
      "status": "created",
      "query": "<string>",
      "entity": {
        "type": "company"
      },
      "criteria": [
        {
          "description": "<string>",
          "successRate": 50
        }
      ],
      "count": 2,
      "progress": {
        "found": 123,
        "completion": 50
      },
      "metadata": {},
      "canceledAt": "2023-11-07T05:31:56Z",
      "canceledReason": "webset_deleted",
      "createdAt": "2023-11-07T05:31:56Z",
      "updatedAt": "2023-11-07T05:31:56Z"
    }
  ],
  "enrichments": [
    {
      "id": "<string>",
      "object": "webset_enrichment",
      "status": "pending",
      "websetId": "<string>",
      "title": "<string>",
      "description": "<string>",
      "format": "text",
      "options": [
        {
          "label": "<string>"
        }
      ],
      "instructions": "<string>",
      "metadata": {},
      "createdAt": "2023-11-07T05:31:56Z",
      "updatedAt": "2023-11-07T05:31:56Z"
    }
  ],
  "metadata": {},
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
"""
def create_webset(query):
    webset = exa.websets.create(
        params=CreateWebsetParameters(
            search={
                "query": query,
                "count": 5
            },
            enrichments=[
                CreateEnrichmentParameters(
                    description="LinkedIn profile of VP of Engineering or related role",
                    format="text",
                ),
            ],
        )
    )

    print(f"Webset created with ID: {webset.id}")

    # Wait until Webset completes processing
    webset = exa.websets.wait_until_idle(webset.id)

    # Retrieve Webset Items
    items = exa.websets.items.list(webset_id=webset.id)
    for item in items.data:
        print(f"Item: {item.model_dump_json(indent=2)}")

    return items.data


def get_webset(webset_id):
    webset = exa.websets.get(webset_id)


    # Wait until Webset completes processing
    #webset = exa.websets.wait_until_idle(webset.id)

    # Retrieve Webset Items
    items = exa.websets.items.list(webset_id=webset_id)
    for item in items.data:
        print(f"Item: {item.model_dump_json(indent=2)}")

    return items.data

def update_webset(webset_id):
    try:
        # Get the existing webset
        webset = exa.websets.get(webset_id)
        if not webset:
            return None

        # Update the webset with new parameters
        # Note: The actual update parameters would depend on what you want to update
        # This is a basic example - you might want to add more parameters
        updated_webset = exa.websets.update(
            webset_id=webset_id,
            params={
                "search": {
                    "query": webset.searches[0].query if webset.searches else "",
                    "count": 5
                },
                "enrichments": [
                    {
                        "description": "LinkedIn profile of VP of Engineering or related role",
                        "format": "text",
                    }
                ]
            }
        )

        # Wait until the update is complete
        updated_webset = exa.websets.wait_until_idle(webset_id)

        # Get the updated items
        items = exa.websets.items.list(webset_id=webset_id)
        return items.data

    except Exception as e:
        print(f"Error updating webset: {str(e)}")
        return None