from django.urls import path
from exaai.views.exa_views import search_ai_blog
from webset.views.webset import create_webset, get_webset, generate_search_criteria

urlpatterns = [
    path('create/', create_webset, name='search_ai_blog'),
    path('get/<webset_id>', get_webset, name='search_ai_blog'),
    path('searchcriteria', generate_search_criteria, name='generate_search_criteria'),
]
