import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
import requests
import os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status

from exaai.utils import result_to_dict
from webset.services import websetService, openAIService
from webset.utils import convert_string_to_json
from webset.constants.api_constants import (
    EXA_WEBSETS_UPDATE_URL,
    EXA_WEBSETS_LIST_URL
)
from webset.utils import get_exa_api_headers
from webset.utils import get_webset_update_payload
from webset.models import APIRequestResponse

load_dotenv()

"""
# Create a Webset with search and enrichments
"""
class CreateWebsetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = websetService.create_webset(request.data)
            return Response({
                'request_id': result['request_id'],
                'message': 'Webset creation initiated',
                'data': result['data']
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetWebsetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, webset_id):
        result = websetService.get_webset(webset_id)
        if result:
            response = {
                "success": True,
                "message": "Webset retrieved successfully",
                "data": json.loads(result[0].model_dump_json())
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                "success": False,
                "message": "Webset retrieval failed",
                "data": []
            }
            return JsonResponse(response, status=400)


class UpdateWebsetsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, webset_id):
        try:
            # Get request data
            request_data = convert_string_to_json(request.body)
            if not request_data:
                return JsonResponse({
                    "success": False,
                    "message": "Request body cannot be empty",
                    "data": []
                }, status=400)

            # Prepare the API call
            url = EXA_WEBSETS_UPDATE_URL.format(webset_id=webset_id)
            payload = get_webset_update_payload(request_data.get('metadata'))
            headers = get_exa_api_headers()

            # Make the API call
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                # Get the updated webset data
                if response.text:
                    response_data = {
                        "success": True,
                        "message": "Webset metadata updated successfully",
                        "data": json.loads( response.text)
                    }
                    return JsonResponse(response_data, status=200)
                else:
                    return JsonResponse({
                        "success": False,
                        "message": "Failed to retrieve updated webset",
                        "data": []
                    }, status=400)
            else:
                return JsonResponse({
                    "success": False,
                    "message": f"Failed to update webset metadata: {response.text}",
                    "data": []
                }, status=response.status_code)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "data": []
            }, status=500)


class GenerateSearchCriteriaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_data = convert_string_to_json(request.body)
            if not request_data:
                raise ValidationError("Empty request body")
            
            query = request_data.get('query')
            if not query:
                return JsonResponse({
                    "success": False,
                    "message": "Query parameter is required",
                    "error": "MISSING_QUERY"
                }, status=400)
            
            result = openAIService.generate_search_criteria(query)
            
            if result.get("success"):
                return JsonResponse({
                    "success": True,
                    "message": result["message"]
                }, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "message": result.get("message", "Search criteria generation failed"),
                    "error": result.get("error", "UNKNOWN_ERROR")
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "An unexpected error occurred",
                "error": str(e)
            }, status=500)


class ListWebsetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Make the API call to list websets
            response = requests.get(
                EXA_WEBSETS_LIST_URL,
                headers=get_exa_api_headers()
            )
            
            if response.status_code == 200:
                response_data = {
                    "success": True,
                    "message": "Websets retrieved successfully",
                    "data": response.json()
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "message": f"Failed to retrieve websets: {response.text}",
                    "data": []
                }, status=response.status_code)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "data": []
            }, status=500)


class WebsetRequestStatusView(APIView):
    def get(self, request, request_id):
        try:
            result = websetService.get_request_status(request_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

