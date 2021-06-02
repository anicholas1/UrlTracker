from rest_framework import serializers
from urltrack.models import UrlTracker


class UrlTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlTracker
        fields = ['url', 'status_code', 'time_checked',
                  'status', 'frequency', 'expected_status']