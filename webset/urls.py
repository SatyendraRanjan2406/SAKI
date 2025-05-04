from django.urls import path
from .views.webset import (
    CreateWebsetView,
    GetWebsetView,
    UpdateWebsetsView,
    GenerateSearchCriteriaView,
    ListWebsetsView,
    WebsetRequestStatusView,
    GetWebsetItemView,
    ListWebsetItemsView,
)
from .views.enrichment import CreateEnrichmentView, GetEnrichmentView, DeleteEnrichmentView
from .views.webhook import GetEventView, CreateWebhookView, UpdateWebhookView, WebhookHandlerView

urlpatterns = [
    path('create/', CreateWebsetView.as_view(), name='create-webset'),
    path('get/<str:webset_id>/', GetWebsetView.as_view(), name='get-webset'),
    path('update/<str:webset_id>/', UpdateWebsetsView.as_view(), name='update-websets'),
    path('generate-search-criteria/', GenerateSearchCriteriaView.as_view(), name='generate-search-criteria'),
    path('list/', ListWebsetsView.as_view(), name='list-websets'),
    path('status/<uuid:request_id>/', WebsetRequestStatusView.as_view(), name='webset-request-status'),
    path('items/<str:webset_id>/<str:item_id>/', GetWebsetItemView.as_view(), name='get-webset-item'),
    path('items/<str:webset_id>/', ListWebsetItemsView.as_view(), name='list-webset-items'),
    path('enrichments/<str:webset_id>/', CreateEnrichmentView.as_view(), name='create-enrichment'),
    path('enrichments/<str:webset_id>/<str:enrichment_id>/', GetEnrichmentView.as_view(), name='get-enrichment'),
    path('enrichments/<str:webset_id>/<str:enrichment_id>/', DeleteEnrichmentView.as_view(), name='delete-enrichment'),
    path('events/<str:event_id>/', GetEventView.as_view(), name='get-event'),
    path('webhooks/', CreateWebhookView.as_view(), name='create-webhook'),
    path('webhooks/<str:webhook_id>/', UpdateWebhookView.as_view(), name='update-webhook'),
    path('webhooks/receive/', WebhookHandlerView.as_view(), name='receive-webhook'),
]
