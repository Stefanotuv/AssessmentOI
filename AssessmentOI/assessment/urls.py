from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # path("", TestView.as_view(template_name='assessment/test.html'), name='test_view'),
    re_path(r'^.*\.html', gentella_html, name='gentella'),

    path("question/", QuestionView.as_view(template_name='assessment/question.html'), name='question_view'),
    path("question/<pk>/detail", QuestionDetailView.as_view(template_name='assessment/question_detail.html'),
         name='question_detail_view'),

    path("assessment/", AssessmentView.as_view(template_name='assessment/assessment.html'), name='assessment_view'),
    path("assessment/<pk>/detail", AssessmentDetailView.as_view(template_name='assessment/assessment_detail.html'),
         name='assessment_detail_view'),
]