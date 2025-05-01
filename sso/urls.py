from django.urls import path, include
from .views import GoogleSSOView, LinkedInSSOView, MicrosoftSSOView

urlpatterns = [
    path('google/', GoogleSSOView.as_view(), {'backend': 'google-oauth2'}),
    path('linkedin/', LinkedInSSOView.as_view(), name='linkedin-sso'),
    path('microsoft/', MicrosoftSSOView.as_view(), name='microsoft-sso'),

] 