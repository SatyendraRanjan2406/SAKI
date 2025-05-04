from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class APIRequestResponse(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_body = models.JSONField()
    response_body = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, failed
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'api_request_response'
        indexes = [
            models.Index(fields=['request_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Request {self.request_id} - {self.status}"

class WebhookData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_id = models.UUIDField(unique=True)
    event = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        db_table = 'webhook_data'
        indexes = [
            models.Index(fields=['request_id']),
            models.Index(fields=['event']),
            models.Index(fields=['status']),
            models.Index(fields=['received_at']),
        ]

    def __str__(self):
        return f"Webhook {self.request_id} - {self.event}"
