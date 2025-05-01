from django.urls import path
from .views.webset import (
    CreateWebsetView,
    GetWebsetView,
    UpdateWebsetsView,
    GenerateSearchCriteriaView,
    ListWebsetsView
)

urlpatterns = [
    path('create/', CreateWebsetView.as_view(), name='create-webset'),
    path('get/<str:webset_id>/', GetWebsetView.as_view(), name='get-webset'),
    path('update/<str:webset_id>/', UpdateWebsetsView.as_view(), name='update-websets'),
    path('generate-search-criteria/', GenerateSearchCriteriaView.as_view(), name='generate-search-criteria'),
    path('list/', ListWebsetsView.as_view(), name='list-websets'),
]
