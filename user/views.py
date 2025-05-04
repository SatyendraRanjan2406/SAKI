from django.http import JsonResponse
from user.services import UserService
from user.exceptions import APIException
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.hashers import make_password
import secrets
import string
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserProfileSerializer,
    UserAddressSerializer
)
from .models import User, UserProfile, UserAddress

User = get_user_model()

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

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                'user': UserDetailSerializer(data['user']).data,
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            logout(request)
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        profile_serializer = UserProfileSerializer(
            request.user.profile,
            data=request.data.get('profile', {}),
            partial=True
        )
        address_serializer = UserAddressSerializer(
            request.user.address,
            data=request.data.get('address', {}),
            partial=True
        )

        if profile_serializer.is_valid() and address_serializer.is_valid():
            profile_serializer.save()
            address_serializer.save()
            return Response(UserDetailSerializer(request.user).data)
        return Response({
            'profile_errors': profile_serializer.errors,
            'address_errors': address_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AdminUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            # Get request data
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            is_admin = request.data.get('is_admin', True)  # Default to admin

            # Validate required fields
            if not username or not email or not password:
                return Response({
                    'error': 'Username, email, and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate API key
            api_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

            # Create user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                is_admin=is_admin,
                api_key=api_key
            )

            return Response({
                'message': 'User created successfully',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'api_key': user.api_key
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Get all admin users
            admin_users = User.objects.filter(is_admin=True)
            
            # Prepare response data
            users_data = [{
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'api_key': user.api_key,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            } for user in admin_users]

            return Response({
                'users': users_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_admin=True)
            
            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'api_key': user.api_key,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'error': 'Admin user not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_admin=True)
            user.delete()
            
            return Response({
                'message': 'Admin user deleted successfully'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'error': 'Admin user not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

