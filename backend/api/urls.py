"""
API URL routing for the Digital Privacy Awareness CEP project.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Survey endpoints
    path('survey/', views.survey_submit, name='survey-submit'),
    path('survey/results/', views.survey_results, name='survey-results'),

    # Quiz endpoints
    path('quiz/', views.quiz_questions, name='quiz-questions'),
    path('quiz/result/', views.quiz_result, name='quiz-result'),
    path('quiz/statistics/', views.quiz_statistics, name='quiz-statistics'),
]
