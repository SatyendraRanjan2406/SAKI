from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from webset.services.webhookService import WebhookService
from webset.models import WebhookData
from datetime import datetime
import uuid

class GetEventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            result = WebhookService.get_event(event_id)
            return Response({
                'request_id': result['request_id'],
                'data': result['data']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateWebhookView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            # Get request data
            events = request.data.get('events', [])
            url = request.data.get('url')
            metadata = request.data.get('metadata', {})
            
            # Validate required fields
            if not events:
                return Response({
                    'error': 'Events list is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            if not url:
                return Response({
                    'error': 'Webhook URL is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create webhook
            result = WebhookService.create_webhook(
                events=events,
                url=url,
                metadata=metadata
            )
            
            return Response({
                'request_id': result['request_id'],
                'data': result['data']
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateWebhookView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, webhook_id):
        try:
            # Get request data
            events = request.data.get('events')
            url = request.data.get('url')
            metadata = request.data.get('metadata')

            # Validate that at least one field is provided
            if events is None and url is None and metadata is None:
                return Response({
                    'error': 'At least one field (events, url, or metadata) must be provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update webhook
            result = WebhookService.update_webhook(
                webhook_id=webhook_id,
                events=events,
                url=url,
                metadata=metadata
            )
            
            return Response({
                'request_id': result['request_id'],
                'data': result['data']
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WebhookHandlerView(APIView):
    def post(self, request):
        try:
            # Extract webhook data
            webhook_data = request.data
            event = webhook_data.get('event')
            webset_id = webhook_data.get('webset_id')
            status = webhook_data.get('status', 'received')
            payload = webhook_data.get('payload', {})
            metadata = webhook_data.get('metadata', {})

            # Validate required fields
            if not event or not webset_id:
                return Response({
                    'error': 'Event and webset_id are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create webhook record
            webhook = WebhookData.objects.create(
                request_id=uuid.uuid4(),  # Generate a new UUID for the webhook
                event=event,
                status=status,
                payload=payload,
                metadata={
                    'webset_id': webset_id,
                    **metadata  # Include any additional metadata
                }
            )

            # Process the webhook (you can add your processing logic here)
            webhook.processed_at = datetime.now()
            webhook.save()

            return Response({
                'message': 'Webhook received and processed successfully',
                'webhook_id': str(webhook.id),
                'request_id': str(webhook.request_id)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # If there's an error, save it with error status
            if 'webhook' in locals():
                webhook.status = 'error'
                webhook.error_message = str(e)
                webhook.save()

            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 