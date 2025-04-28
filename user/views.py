from django.http import JsonResponse
from user.services import UserService
from user.exceptions import APIException
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class UserInfoView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            user = UserService.get_authenticated_user(request)
            data = UserService.get_user_info(user)
            return JsonResponse({"success": True, "data": data}, status=200)
        except APIException as e:
            return JsonResponse({"success": False, "message": e.message}, status=e.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

