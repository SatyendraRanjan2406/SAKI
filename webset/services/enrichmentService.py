import requests
from webset.constants.api_constants import (
    EXA_WEBSETS_ENRICHMENTS_CREATE_URL,
    EXA_WEBSETS_ENRICHMENTS_GET_URL
)
from webset.utils import get_exa_api_headers, get_enrichment_payload
from webset.models import APIRequestResponse

class EnrichmentService:
    @staticmethod
    def create_enrichment(webset_id, description, format_type="text", options=None, metadata=None):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "webset_id": webset_id,
                    "description": description,
                    "format": format_type,
                    "options": options,
                    "metadata": metadata
                }
            )
            
            # Prepare the request
            url = EXA_WEBSETS_ENRICHMENTS_CREATE_URL.format(webset_id=webset_id)
            headers = get_exa_api_headers()
            payload = get_enrichment_payload(description, format_type, options, metadata)
            
            # Make the API request
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Update the request record with the response
            request_record.response_body = response_data
            request_record.status = 'completed'
            request_record.save()
            
            return {
                'request_id': str(request_record.request_id),
                'data': response_data
            }
            
        except requests.exceptions.RequestException as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error creating enrichment: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing enrichment request: {str(e)}")

    @staticmethod
    def get_enrichment(webset_id, enrichment_id):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "webset_id": webset_id,
                    "enrichment_id": enrichment_id
                }
            )
            
            # Prepare the request
            url = EXA_WEBSETS_ENRICHMENTS_GET_URL.format(
                webset_id=webset_id,
                enrichment_id=enrichment_id
            )
            headers = get_exa_api_headers()
            
            # Make the API request
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Update the request record with the response
            request_record.response_body = response_data
            request_record.status = 'completed'
            request_record.save()
            
            return {
                'request_id': str(request_record.request_id),
                'data': response_data
            }
            
        except requests.exceptions.RequestException as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error fetching enrichment: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing enrichment request: {str(e)}")

    @staticmethod
    def delete_enrichment(webset_id, enrichment_id):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "webset_id": webset_id,
                    "enrichment_id": enrichment_id,
                    "action": "delete"
                }
            )
            
            # Prepare the request
            url = EXA_WEBSETS_ENRICHMENTS_GET_URL.format(
                webset_id=webset_id,
                enrichment_id=enrichment_id
            )
            headers = get_exa_api_headers()
            
            # Make the API request
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Update the request record with the response
            request_record.response_body = response_data
            request_record.status = 'completed'
            request_record.save()
            
            return {
                'request_id': str(request_record.request_id),
                'data': response_data
            }
            
        except requests.exceptions.RequestException as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error deleting enrichment: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing enrichment deletion request: {str(e)}") 