from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from exaai.utils import result_to_dict
from webset.services import websetService
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