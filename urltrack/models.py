from django.db import models
from django.contrib.auth.models import User


class UrlTracker(models.Model):
    url = models.CharField(max_length=255)
    frequency = models.IntegerField(default=60)
    expected_status = models.IntegerField(default=200)
    admin_email = models.CharField(max_length=255, blank=True, null=True)
    user_emails = models.TextField(blank=True, default=None, null=True)  # JSON field for all emails
    failed_status = models.IntegerField(default=0)
    last_checked = models.DateTimeField(blank=True, null=True)


class UrlStatus(models.Model):
    url_tracker = models.ForeignKey(UrlTracker, on_delete=models.SET_NULL, null=True)
    status_code = models.IntegerField()
    time_checked = models.DateTimeField()
    state = models.BooleanField(default=False)


