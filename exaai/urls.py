from django.urls import path
from .views.exa_views import SearchAIBlogView

urlpatterns = [
    path('search/', SearchAIBlogView.as_view(), name='search-ai-blog'),
]
