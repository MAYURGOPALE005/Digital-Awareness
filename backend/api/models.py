"""
Models for the Digital Privacy Awareness CEP project.
Stores survey responses and quiz results collected from community members.
"""

from django.db import models


class SurveyResponse(models.Model):
    """
    Stores one survey submission from a community member.
    No personally identifiable information is collected.
    """

    AGE_GROUP_CHOICES = [
        ('under_18', 'Under 18'),
        ('18_25', '18 – 25'),
        ('26_35', '26 – 35'),
        ('36_50', '36 – 50'),
        ('above_50', 'Above 50'),
    ]

    INTERNET_USAGE_CHOICES = [
        ('rarely', 'Rarely'),
        ('few_times_week', 'A few times a week'),
        ('daily', 'Daily'),
        ('multiple_hours', 'Multiple hours every day'),
    ]

    AWARENESS_CHOICES = [
        ('not_aware', 'Not Aware'),
        ('slightly_aware', 'Slightly Aware'),
        ('moderately_aware', 'Moderately Aware'),
        ('very_aware', 'Very Aware'),
    ]

    PRACTICE_CHOICES = [
        ('never', 'Never'),
        ('rarely', 'Rarely'),
        ('sometimes', 'Sometimes'),
        ('always', 'Always'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure'),
    ]

    age_group = models.CharField(
        max_length=20,
        choices=AGE_GROUP_CHOICES,
        verbose_name='Age Group',
    )
    internet_usage = models.CharField(
        max_length=30,
        choices=INTERNET_USAGE_CHOICES,
        verbose_name='Internet Usage Frequency',
    )
    platforms = models.TextField(
        verbose_name='Frequently Used Digital Platforms',
        help_text='Comma-separated list of platforms',
    )
    privacy_awareness = models.CharField(
        max_length=20,
        choices=AWARENESS_CHOICES,
        verbose_name='Digital Privacy Awareness Level',
    )
    password_practice = models.CharField(
        max_length=20,
        choices=PRACTICE_CHOICES,
        verbose_name='Password Practices',
    )
    two_factor_auth = models.CharField(
        max_length=20,
        choices=YES_NO_CHOICES,
        verbose_name='Uses Two-Factor Authentication',
    )
    phishing_awareness = models.CharField(
        max_length=20,
        choices=AWARENESS_CHOICES,
        verbose_name='Phishing Awareness',
    )
    app_permissions = models.CharField(
        max_length=20,
        choices=PRACTICE_CHOICES,
        verbose_name='App Permission Practices',
    )
    social_media_privacy = models.CharField(
        max_length=20,
        choices=PRACTICE_CHOICES,
        verbose_name='Social Media Privacy Practices',
    )
    online_payment_safety = models.CharField(
        max_length=20,
        choices=PRACTICE_CHOICES,
        verbose_name='Online Payment Safety',
    )
    privacy_concern = models.TextField(
        verbose_name='Biggest Digital Privacy Concern',
        blank=True,
        default='',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'

    def __str__(self):
        return f"Survey #{self.pk} — {self.age_group} — {self.created_at:%Y-%m-%d}"


class QuizResult(models.Model):
    """
    Stores one quiz attempt result.
    """

    LEVEL_CHOICES = [
        ('needs_improvement', 'Needs Improvement'),
        ('moderate', 'Moderate Awareness'),
        ('good', 'Good Privacy Awareness'),
    ]

    score = models.IntegerField(verbose_name='Score')
    total_questions = models.IntegerField(default=10, verbose_name='Total Questions')
    percentage = models.FloatField(verbose_name='Percentage')
    awareness_level = models.CharField(
        max_length=30,
        choices=LEVEL_CHOICES,
        verbose_name='Awareness Level',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quiz Result'
        verbose_name_plural = 'Quiz Results'

    def __str__(self):
        return f"Quiz #{self.pk} — {self.score}/{self.total_questions} — {self.awareness_level}"
