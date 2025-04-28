from user.models import User

class UserService:
    @staticmethod
    def get_authenticated_user(request):
        if not request.user.is_authenticated:
            from user.exceptions import UnauthorizedException
            raise UnauthorizedException()
        return request.user

    @staticmethod
    def get_user_info(user):
        return {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
