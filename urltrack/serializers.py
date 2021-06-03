from rest_framework import serializers
from urltrack.models import UrlTracker, UrlStatus
from email_validator import validate_email, EmailNotValidError


class UrlTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlTracker
        fields = ['url', 'frequency', 'expected_status', 'admin_email', 'user_emails']

    def validate_url(self, value):
        if 'http://' in value or 'https://' in value:
            return value
        raise serializers.ValidationError("Url must contain http or https://")

    def validate_admin_email(self, value):
        try:
            valid = validate_email(value)
            return valid.email
        except EmailNotValidError:
            raise serializers.ValidationError("Email is not valid")


class UrlStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlStatus
        fields = ['url_tracker', 'status_code',
                  'time_checked',
                  'state'
                  ]
