from django.db import models
from django.contrib.auth.models import User


class UrlTracker(models.Model):
    url = models.CharField(max_length=255)
    status_code = models.IntegerField(blank=True, null=True)
    time_checked = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    frequency = models.IntegerField(default=60)
    expected_status = models.IntegerField(default=200)

    # account = models.ForeignKey(User, on_delete=models.CASCADE)