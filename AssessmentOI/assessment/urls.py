from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # path("", TestView.as_view(template_name='assessment/test.html'), name='test_view'),
    re_path(r'^.*\.html', gentella_html, name='gentella'),

    # path("question/", QuestionView.as_view(template_name='assessment/question.html'), name='question_view'),
    # path("question/<pk>/detail", QuestionDetailView.as_view(template_name='assessment/question_detail.html'),
    #      name='question_detail_view'),
    #
    # path("assessment/", AssessmentView.as_view(template_name='assessment/assessment.html'), name='assessment_view'),
    # path("assessment/<pk>/detail", AssessmentDetailView.as_view(template_name='assessment/assessment_detail.html'),
    #      name='assessment_detail_view'),
    #
    # path("validate_token/", ValidateTokenView.as_view(template_name='assessment/validate_token.html'),
    #      name='validate_token_view'),
    #
    # path("test/test_launch/<slug:token>", TestQuestionsView.as_view(template_name='assessment/test_launch.html'),
    #      name='test_launch_view'),
    # path("test/test_questions/<slug:token>", TestQuestionsView.as_view(template_name='assessment/test_questions.html'),
    #      name='test_questions_view'),
    #
    # path("test/submit/<slug:token>", TestQuestionsSubmitUpdate.as_view(template_name='assessment/test_questions_submit.html'),
    #      name='test_questions_submit_view'),
    #
    # path("test/home/<slug:token>", Home.as_view(template_name='assessment/home.html'),
    #      name='home_view'),
    # path("test/practice_questions/<slug:token>", PracticeQuestionsView.as_view(template_name='assessment/practice_questions.html'),
    #     name='practice_questions_view'),
    #
    # path("manager/assessment/assessment_file_upload",AssessmentView.as_view(template_name='assessment/manager/assessment_file_upload.html'),
    #      name='assessment_file_upload_view'),

    path("home", HomeView.as_view(template_name='assessment/director/home.html'),
         name='home_view'),

    # Candidate classes

    path("candidate/home", CandidateHomeView.as_view(template_name='assessment/candidate/home.html'),
         name='candidate_home_view'),

    path("candidate/practice_test", PracticeQuestionsView.as_view(template_name='assessment/candidate/practice_test.html'),
         name='practice_test_view'),

    path("candidate/test", TestHomeView.as_view(template_name='assessment/candidate/test_home.html'),
         name='test_home_view'),

    path("candidate/test/test_questions/<slug:token>", TestCandidateQuestionsView.as_view(template_name='assessment/candidate/test_questions.html'),
         name='test_questions_view'),

    path("candidate/test/submit/<slug:token>", TestQuestionsSubmitUpdate.as_view(template_name='assessment/candidate/test_questions_submit.html'),
         name='test_questions_submit_view'),


    path("candidate/test/token_validated/<slug:token>", TestTokenValidatedView.as_view(template_name='assessment/candidate/test_token_validated.html'),
         name='test_token_validated_view'),

    # Director classes

    path("director/dashboard", DashboardView.as_view(template_name='assessment/director/dashboard.html'),
         name='dashboard_view'),
    path("director/assessment/", AssessmentListView.as_view(template_name='assessment/director/assessment_list.html'),
         name='assessment_list_view'),

    path("director/assessment/create",
         AssessmentCreateView.as_view(template_name='assessment/director/assessment_create.html'),
         name='assessment_create_view'),

    path("director/assessment/<pk>/detail", AssessmentDetailView.as_view(template_name='assessment/director/assessment_detail.html'),
         name='assessment_detail_view'),

    path("director/question/create", QuestionCreateView.as_view(template_name='assessment/director/question_create.html'),
         name='question_create_view'),

    path("director/question/upload_from_file",
         QuestionCreateFromFileView.as_view(template_name='assessment/director/question_upload_from_file.html'),
         name='question_upload_from_file_view'),

    path("director/question/uploaded",
         QuestionUploadedView.as_view(template_name='assessment/director/question_uploaded.html'),
         name='question_uploaded_view'),

    path("director/question/", QuestionListView.as_view(template_name='assessment/director/question_list.html'), name='question_list_view'),

    path("director/question/<pk>/detail", QuestionDetailView.as_view(template_name='assessment/director/question_detail.html'),
         name='question_detail_view'),
]