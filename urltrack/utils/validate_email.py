from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers


def validate_user_email(value):
    try:
        valid = validate_email(value)
        return valid.email
    except EmailNotValidError:
        raise serializers.ValidationError("Email is not valid")