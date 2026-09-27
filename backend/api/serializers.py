"""
DRF Serializers for the Digital Privacy Awareness CEP project.
"""

from rest_framework import serializers
from .models import SurveyResponse, QuizResult


class SurveyResponseSerializer(serializers.ModelSerializer):
    """Validates and serializes survey submission data."""

    class Meta:
        model = SurveyResponse
        fields = [
            'id',
            'age_group',
            'internet_usage',
            'platforms',
            'privacy_awareness',
            'password_practice',
            'two_factor_auth',
            'phishing_awareness',
            'app_permissions',
            'social_media_privacy',
            'online_payment_safety',
            'privacy_concern',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class QuizResultSerializer(serializers.ModelSerializer):
    """Validates and serializes quiz result data."""

    class Meta:
        model = QuizResult
        fields = [
            'id',
            'score',
            'total_questions',
            'percentage',
            'awareness_level',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Score must be between 0 and 10.")
        return value

    def validate_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Percentage must be between 0 and 100.")
        return value
