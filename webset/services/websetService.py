import os

from dotenv import load_dotenv
from exa_py import Exa
from exa_py.websets.types import CreateWebsetParameters, CreateEnrichmentParameters

from webset.tasks import create_webset_task
from webset.models import APIRequestResponse
import uuid
import json
from django.core.serializers.json import DjangoJSONEncoder

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

class websetService:
    @staticmethod
    def create_webset(request_data):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body=request_data
            )
            
            # Your existing create_webset logic here
            # For example:
            response_data = {
                # ... your existing response data ...
            }
            
            # Update the request record with the response
            request_record.response_body = response_data
            request_record.status = 'completed'
            request_record.save()
            
            # Return response with request_id
            return {
                'request_id': str(request_record.request_id),
                'data': response_data
            }
            
        except Exception as e:
            # Update request record with error
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            
            raise Exception(f"Error creating webset: {str(e)}")

    @staticmethod
    def get_request_status(request_id):
        try:
            request_record = APIRequestResponse.objects.get(request_id=request_id)
            return {
                'request_id': str(request_record.request_id),
                'status': request_record.status,
                'response': request_record.response_body,
                'error': request_record.error_message,
                'created_at': request_record.created_at,
                'updated_at': request_record.updated_at
            }
        except APIRequestResponse.DoesNotExist:
            raise Exception(f"Request with ID {request_id} not found")
        except Exception as e:
            raise Exception(f"Error retrieving request status: {str(e)}")

def create_webset(request_data):
    try:
        # Create a new request record
        request_record = APIRequestResponse.objects.create(
            request_body=request_data
        )

        # Your existing create_webset logic here
        # For example:
        response_data = {
            # ... your existing response data ...
        }
         # create_webset_task.delay(query)
        from exa_py.websets.types import CreateWebsetParameters, CreateEnrichmentParameters

        from webset.services.websetService import exa
        webset = exa.websets.create(
            params=CreateWebsetParameters(
                search={
                    "query": request_data["query"],
                    "count": 5
                },
                # enrichments=[
                #     CreateEnrichmentParameters(
                #         description="LinkedIn profile of VP of Engineering or related role",
                #         format="text",
                #     ),
                # ],
            )
        )

        print(f"Webset created with ID: {webset.id}")

        # Wait until Webset completes processing
        webset = exa.websets.wait_until_idle(webset.id)

        # Retrieve Webset Items
        items = exa.websets.items.list(webset_id=webset.id)
        for item in items.data:
            print(f"Item: {item.model_dump_json(indent=2)}")

        response_data= json.loads(items.model_dump_json())


        # Update the request record with the response
        request_record.response_body = json.dumps(response_data,default=vars)
        request_record.status = 'completed'
        request_record.save()

        # Return response with request_id
        return {
            'request_id': str(request_record.request_id),
            'data': response_data
        }

    except Exception as e:
        # Update request record with error
        if 'request_record' in locals():
            request_record.status = 'failed'
            request_record.error_message = str(e)
            request_record.save()

        raise Exception(f"Error creating webset: {str(e)}")
    # create_webset_task.delay(query)


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
            id=webset_id,
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
        items = updated_webset.list(webset_id=webset_id)
        return  json.loads(items.model_dump_json())

    except Exception as e:
        print(f"Error updating webset: {str(e)}")
        return None