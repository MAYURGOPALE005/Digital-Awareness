"""
Django admin registration for the Digital Privacy Awareness CEP project.
"""

from django.contrib import admin
from .models import SurveyResponse, QuizResult


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'age_group', 'privacy_awareness', 'created_at']
    list_filter = ['age_group', 'privacy_awareness', 'created_at']
    readonly_fields = ['created_at']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'percentage', 'awareness_level', 'created_at']
    list_filter = ['awareness_level', 'created_at']
    readonly_fields = ['created_at']
