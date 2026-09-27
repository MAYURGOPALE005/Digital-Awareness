"""
URL configuration for Digital Privacy Awareness CEP project.
Serves both the API endpoints and frontend HTML pages.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # REST API endpoints
    path('api/', include('api.urls')),

    # Frontend pages served by Django
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('learn/', TemplateView.as_view(template_name='learn.html'), name='learn'),
    path('quiz/', TemplateView.as_view(template_name='quiz.html'), name='quiz'),
    path('tips/', TemplateView.as_view(template_name='tips.html'), name='tips'),
    path('survey/', TemplateView.as_view(template_name='survey.html'), name='survey'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
