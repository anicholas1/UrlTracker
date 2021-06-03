from rest_framework import serializers
from urltrack.models import UrlTracker, UrlStatus


class UrlTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlTracker
        fields = ['url', 'frequency', 'expected_status', 'admin_email']


class UrlStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlStatus
        fields = ['url_tracker', 'status_code',
                  'time_checked',
                  'state'
                  ]
