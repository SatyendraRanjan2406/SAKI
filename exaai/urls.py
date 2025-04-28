from django.urls import path
from exaai.views.exa_views import search_ai_blog

urlpatterns = [
    path('search/', search_ai_blog, name='search_ai_blog'),
]
