from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa, load_strategy, load_backend
from user.models import User, UserProfile
from user.serializers import UserDetailSerializer

class SSOBaseView(APIView):
    def get_or_create_user(self, user_data):
        email = user_data.get('email')
        if not email:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                is_active=True
            )
            # Create user profile
            UserProfile.objects.create(
                user=user,
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', '')
            )
        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

class GoogleSSOView(SSOBaseView):
    authentication_classes = []
    permission_classes = []
    def post(self, request,  *args, **kwargs):
        try:
            django_request = request._request  # unwrap DRF request

            # Add access_token to request.POST
            django_request.POST = django_request.POST.copy()
            django_request.POST['access_token'] = request.data.get('access_token')
            # Inject backend name
            backend = kwargs.get('backend')

            # Load the backend
            strategy = load_strategy(django_request)
            backend_instance = load_backend(strategy=strategy, name=backend, redirect_uri=None)

            user = backend_instance.do_auth(request.data.get('access_token'))
            if user and user.is_active:
                tokens = self.get_tokens_for_user(user)
                return Response({
                    'user': UserDetailSerializer(user).data,
                    **tokens
                })
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LinkedInSSOView(SSOBaseView):
    @psa('social:complete')
    def post(self, request, backend):
        try:
            user = request.backend.do_auth(request.data.get('access_token'))
            if user and user.is_active:
                tokens = self.get_tokens_for_user(user)
                return Response({
                    'user': UserDetailSerializer(user).data,
                    **tokens
                })
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MicrosoftSSOView(SSOBaseView):
    @psa('social:complete')
    def post(self, request, backend):
        try:
            user = request.backend.do_auth(request.data.get('access_token'))
            if user and user.is_active:
                tokens = self.get_tokens_for_user(user)
                return Response({
                    'user': UserDetailSerializer(user).data,
                    **tokens
                })
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
