import requests
from webset.constants.api_constants import (
    EXA_WEBSETS_EVENTS_GET_URL,
    EXA_WEBSETS_WEBHOOKS_CREATE_URL,
    EXA_WEBSETS_WEBHOOKS_UPDATE_URL
)
from webset.utils import get_exa_api_headers, get_webhook_payload
from webset.models import APIRequestResponse

class WebhookService:
    @staticmethod
    def get_event(event_id):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "event_id": event_id,
                    "action": "get_event"
                }
            )
            
            # Prepare the request
            url = EXA_WEBSETS_EVENTS_GET_URL.format(event_id=event_id)
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
            raise Exception(f"Error fetching event: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing event request: {str(e)}")

    @staticmethod
    def create_webhook(events, url, metadata=None):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "events": events,
                    "url": url,
                    "metadata": metadata
                }
            )
            
            # Prepare the request
            headers = get_exa_api_headers()
            payload = get_webhook_payload(events, url, metadata)
            
            # Make the API request
            response = requests.post(
                EXA_WEBSETS_WEBHOOKS_CREATE_URL,
                json=payload,
                headers=headers
            )
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
            raise Exception(f"Error creating webhook: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing webhook creation request: {str(e)}")

    @staticmethod
    def update_webhook(webhook_id, events=None, url=None, metadata=None):
        try:
            # Create a new request record
            request_record = APIRequestResponse.objects.create(
                request_body={
                    "webhook_id": webhook_id,
                    "events": events,
                    "url": url,
                    "metadata": metadata
                }
            )
            
            # Prepare the request
            headers = get_exa_api_headers()
            payload = {}
            
            # Only include fields that are provided
            if events is not None:
                payload['events'] = events
            if url is not None:
                payload['url'] = url
            if metadata is not None:
                payload['metadata'] = metadata
            
            # Make the API request
            url = EXA_WEBSETS_WEBHOOKS_UPDATE_URL.format(webhook_id=webhook_id)
            response = requests.patch(
                url,
                json=payload,
                headers=headers
            )
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
            raise Exception(f"Error updating webhook: {str(e)}")
        except Exception as e:
            if 'request_record' in locals():
                request_record.status = 'failed'
                request_record.error_message = str(e)
                request_record.save()
            raise Exception(f"Error processing webhook update request: {str(e)}") 