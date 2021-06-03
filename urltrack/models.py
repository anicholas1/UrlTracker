from django.db import models
from django.contrib.auth.models import User


class UrlTracker(models.Model):
    # TODO Add account and email field
    url = models.CharField(max_length=255)
    frequency = models.IntegerField(default=60)
    expected_status = models.IntegerField(default=200)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # creator of tracker
    users = models.TextField(blank=True, default=None, null=True)  # JSON field for all emails
    failed_status = models.IntegerField(default=0)


class UrlStatus(models.Model):
    url_tracker = models.ForeignKey(UrlTracker, on_delete=models.SET_NULL, null=True)
    status_code = models.IntegerField()
    time_checked = models.DateTimeField()
    state = models.BooleanField(default=False)


