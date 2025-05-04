from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from webset.services.enrichmentService import EnrichmentService

class CreateEnrichmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, webset_id):
        try:
            # Get request data
            description = request.data.get('description')
            format_type = request.data.get('format', 'text')
            options = request.data.get('options', [])
            metadata = request.data.get('metadata', {})
            
            # Validate required fields
            if not description:
                return Response({
                    'error': 'Description is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create enrichment
            result = EnrichmentService.create_enrichment(
                webset_id=webset_id,
                description=description,
                format_type=format_type,
                options=options,
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

class GetEnrichmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, webset_id, enrichment_id):
        try:
            result = EnrichmentService.get_enrichment(webset_id, enrichment_id)
            return Response({
                'request_id': result['request_id'],
                'data': result['data']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteEnrichmentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, webset_id, enrichment_id):
        try:
            result = EnrichmentService.delete_enrichment(webset_id, enrichment_id)
            return Response({
                'request_id': result['request_id'],
                'data': result['data']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 