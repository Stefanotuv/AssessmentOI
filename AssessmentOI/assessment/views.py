from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('gentelella/' + load_template)
    return HttpResponse(template.render(context, request))

@method_decorator(login_required, name='dispatch')
class AssessmentView(ListView):
    model = Assessment
    template_name = 'assessment/assessment.html'
    context_object_name = 'assessment_view'
    pass

@method_decorator(login_required, name='dispatch')
class TestQuestionsView(DetailView):
    model = Assessment
    template_name = 'assessment/test_questions.html'
    context_object_name = 'test_questions_view'
    slug_field = 'token'
    slug_url_kwarg = 'token'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['assessment'] = Assessment.objects.filter(assessment=self.kwargs['pk'])
        pk = Assessment.objects.filter(token=self.kwargs['token'])[0].pk
        questions_selected = Question.objects.filter(assessment__pk=pk)
        context['questions_selected'] = questions_selected

        # total number of questions
        number_of_questions = questions_selected.count()
        context['number_of_questions'] = number_of_questions

        # create a range to be used by the template to identify the question mumber
        number_of_questions_range = range(number_of_questions)
        context['number_of_questions_range'] = number_of_questions_range
        count = 1
        dict_output = {}
        for Q in questions_selected:
            dict_output [count] = Q
            count = count+1
        context['dict_output'] = dict_output
        return context

    # def post(self, request, *args, **kwargs):
    #     HttpResponseRedirect(reverse('test_questions_view'))
    #     pass
    def post(self,request, *args, **kwargs):

        return self.get(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        token = self.kwargs['token']
        # token = request.POST['token']

        # query token and user to see if the candidate has an assessment assigned

        # test if it exist pass user and token (the token is unique... but we want to verify the correct email too)
        assessment_query = Assessment.objects.filter(token=token)
        if assessment_query:
            assessment = Assessment.objects.filter(token=token)[0]
            if assessment.candidate_email == request.user.email:
                if assessment.completed == 'Yes':
                    return HttpResponseRedirect(reverse('home_view',kwargs = {'token': token}))
                else:
                    return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('validate_token_view'))
        else:
            return HttpResponseRedirect(reverse('validate_token_view'))

        # check if the token and the user are valid at the same time.

@method_decorator(login_required, name='dispatch')
class PracticeQuestionsView(DetailView):
    model = Assessment
    template_name = 'assessment/test_questions.html'
    context_object_name = 'test_questions_view'
    slug_field = 'token'
    slug_url_kwarg = 'token'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['assessment'] = Assessment.objects.filter(assessment=self.kwargs['pk'])
        pk = Assessment.objects.filter(token=self.kwargs['token'])[0].pk
        questions_selected = Question.objects.filter(assessment__pk=pk)
        context['questions_selected'] = questions_selected

        # total number of questions
        number_of_questions = questions_selected.count()
        context['number_of_questions'] = number_of_questions

        # create a range to be used by the template to identify the question mumber
        number_of_questions_range = range(number_of_questions)
        context['number_of_questions_range'] = number_of_questions_range
        count = 1
        dict_output = {}
        for Q in questions_selected:
            dict_output [count] = Q
            count = count+1
        context['dict_output'] = dict_output
        return context

    # def post(self, request, *args, **kwargs):
    #     HttpResponseRedirect(reverse('test_questions_view'))
    #     pass
    def post(self,request, *args, **kwargs):

        return self.get(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        # token = 'Test_Token'

        # return HttpResponseRedirect(reverse('home_view',kwargs = {'token': token}))
        return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TestQuestionsSubmitUpdate(UpdateView):
    model = Assessment
    template_name = 'assessment/test_questions_submit.html'
    context_object_name = 'test_questions_submit_view'
    # fields = '__all__'
    form_class = AssessmentForm
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment'] = Assessment.objects.filter(token=self.kwargs['token'])[0]

        return context

    def post(self, request, *args, **kwargs):
        token = self.kwargs['token']
        test = Assessment.objects.filter(token=token)[0]
        # [values.append(value) for value in request.POST]
        answers = {}
        for element in request.POST.items():
            answer_list = []
            if element[0].startswith('Q'):
                if "-" in element[0]:
                    question_number = element[0].split('-')[0]
                    answer_number = element[1]
                    answer_list.append(answer_number)
                    # check if the question already exist and hence is a multiple choice
                    if question_number in answers:
                        answers[question_number].append(answer_number)
                    else:
                        answers[question_number] = answer_list
                else:
                    question_number = element[0]
                    answer_number = element[1]
                    answer_list.append(answer_number)
                    answers[question_number]= answer_list
                    pass
        # we should test if it comes from a valid form (it maybe access directly from the URL?)

        # Register information, answers and result
        if test.completed != 'Yes':
            test.date_complete = datetime.now()
            test.completed = 'Yes'
            test.answers = answers
            test.save()

        return HttpResponseRedirect(reverse('test_questions_submit_view',kwargs = {'token': token}))

    def calculate_score(self,assessment,answers):
        pass
    pass

@method_decorator(login_required, name='dispatch')
class AssessmentDetailView(DetailView):
    model = Assessment
    template_name = 'assessment/assessment_detail.html'
    context_object_name = 'assessment_detail_view'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['assessment'] = Assessment.objects.filter(assessment=self.kwargs['pk'])
        questions_selected = Question.objects.filter(assessment__pk=self.object.pk)
        context['questions_selected'] = questions_selected
        return context

@method_decorator(login_required, name='dispatch')
class QuestionView(ListView):
    model = Question
    template_name = 'assessment/question.html'
    context_object_name = 'question_view'

    # ordering = ['-date_elaboration']
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class QuestionDetailView(DetailView):
    model = Question
    # fields = '_all_'
    template_name = 'assessment/question_detail.html'
    context_object_name = 'question_detail_view'


    def get_queryset(self):
        self.obj = get_object_or_404(Question, pk=self.kwargs['pk'])
        return Question.objects.filter(pk=self.obj.pk)

@method_decorator(login_required, name='dispatch')
class ValidateTokenView(ListView):
    model = Assessment
    template_name = 'assessment/validate_token.html'
    context_object_name = 'validate_token_view'
    # fields = '__all__'
    # form_class = AssessmentForm
    # slug_field = 'token'
    # slug_url_kwarg = 'token'
    def post(self, request, *args, **kwargs):

        token = request.POST['token']

        # query token and user to see if the candidate has an assessment assigned

        # test if it exist pass user and token (the token is unique... but we want to verify the correct email too)
        assessment_query = Assessment.objects.filter(token=token)
        if assessment_query:
            assessment = Assessment.objects.filter(token=token)[0]
            if assessment.candidate_email == request.user.email:
                return HttpResponseRedirect(reverse('home_view', kwargs={'token': token}))
            else:
                return HttpResponseRedirect(reverse('validate_token_view'))
        else:
            return HttpResponseRedirect(reverse('validate_token_view'))

@method_decorator(login_required, name='dispatch')
class Home(UpdateView):
        model = Assessment
        template_name = 'assessment/test_questions_submit.html'
        context_object_name = 'test_questions_submit_view'
        # fields = '__all__'
        form_class = AssessmentForm
        slug_field = 'token'
        slug_url_kwarg = 'token'

        def get_context_data(self, **kwargs):
            token = self.kwargs['token']
            context = super().get_context_data(**kwargs)
            context['assessment'] = Assessment.objects.filter(token=token)[0]

            return context
        def get(self,request, *args, **kwargs):
            token = self.kwargs['token']
            # token = request.POST['token']

            # query token and user to see if the candidate has an assessment assigned

            # test if it exist pass user and token (the token is unique... but we want to verify the correct email too)
            assessment_query = Assessment.objects.filter(token=token)
            if assessment_query:
                assessment = Assessment.objects.filter(token=token)[0]
                if assessment.candidate_email == request.user.email:
                    return super().get(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse('validate_token_view'))
            else:
                return HttpResponseRedirect(reverse('validate_token_view'))

        def post(self, request, *args, **kwargs):
            token = self.kwargs['token']
            test = Assessment.objects.filter(token=token)[0]
            # [values.append(value) for value in request.POST]
            answers = {}
            for element in request.POST.items():
                answer_list = []
                if element[0].startswith('Q'):
                    if "-" in element[0]:
                        question_number = element[0].split('-')[0]
                        answer_number = element[1]
                        answer_list.append(answer_number)
                        # check if the question already exist and hence is a multiple choice
                        if question_number in answers:
                            answers[question_number].append(answer_number)
                        else:
                            answers[question_number] = answer_list
                    else:
                        question_number = element[0]
                        answer_number = element[1]
                        answer_list.append(answer_number)
                        answers[question_number] = answer_list
                        pass
            # we should test if it comes from a valid form (it maybe access directly from the URL?)

            # Register information, answers and result
            if test.completed != 'Yes':
                test.date_complete = datetime.now()
                test.completed = 'Yes'
                test.answers = answers
                test.save()

            return HttpResponseRedirect(reverse('test_questions_submit_view', kwargs={'token': token}))

        def calculate_score(self, assessment, answers):
            pass

        pass