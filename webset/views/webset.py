from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from exaai.utils import result_to_dict
from webset.services import websetService, openAIService
from webset.utils import convert_string_to_json


"""
# Create a Webset with search and enrichments
"""
@csrf_exempt
def create_webset(request):
    if request.method == "POST":
        query = convert_string_to_json(request.body).get('query')
        if query is None:
            return JsonResponse({'status': 'error', 'message': 'No query provided'},status=400)
        # TO BE CHECKED
        result = websetService.create_webset(query)
        if result :
            response = {
                "success": True,
                "message": "Webset created successfully",
                "data": result_to_dict(result)
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                "success": False,
                "message": "Webset creation failed",
                "data": []
            }
            return JsonResponse(response, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'},status=405)


def get_webset(request,webset_id):
    if request.method == "GET":
        # TO BE CHECKED
        result = websetService.get_webset(webset_id)
        if result:
            response = {
                "success": True,
                "message": "Webset created successfully",
                "data": result_to_dict(result)
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                "success": False,
                "message": "Webset creation failed",
                "data": []
            }
            return JsonResponse(response, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def list_websets(request,webset_id):
    if request.method == "POST":
        # TO BE CHECKED
        result = websetService.update_webset(webset_id)
        if result:
            response = {
                "success": True,
                "message": "Webset created successfully",
                "data": result_to_dict(result)
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                "success": False,
                "message": "Webset creation failed",
                "data": []
            }
            return JsonResponse(response, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def generate_search_criteria(request):
    """
    Generate search criteria using OpenAI.
    
    Expected request format:
    {
        "query": "string"  # The search query
    }
    
    Returns:
        JsonResponse with structure:
        {
            "success": bool,
            "message": list/str,
            "error": str (optional)
        }
    """
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed",
            "error": "METHOD_NOT_ALLOWED"
        }, status=405)
    
    try:
        # Parse request body
        try:
            request_data = convert_string_to_json(request.body)
            if not request_data:
                raise ValidationError("Empty request body")
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "Invalid request format",
                "error": str(e)
            }, status=400)
        
        # Validate query parameter
        query = request_data.get('query')
        if not query:
            return JsonResponse({
                "success": False,
                "message": "Query parameter is required",
                "error": "MISSING_QUERY"
            }, status=400)
        
        # Generate search criteria
        result = openAIService.generate_search_criteria(query)
        
        # Handle the response
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

