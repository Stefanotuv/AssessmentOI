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



def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('gentelella/' + load_template)
    return HttpResponse(template.render(context, request))


class AssessmentView(ListView):
    model = Assessment
    template_name = 'assessment/assessment.html'
    context_object_name = 'assessment_view'
    pass

# test_questions
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

    def get(self,request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        pass

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


class QuestionView(ListView):
    model = Question
    template_name = 'assessment/question.html'
    context_object_name = 'question_view'

    # ordering = ['-date_elaboration']
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class QuestionDetailView(DetailView):
    model = Question
    # fields = '_all_'
    template_name = 'assessment/question_detail.html'
    context_object_name = 'question_detail_view'


    def get_queryset(self):
        self.obj = get_object_or_404(Question, pk=self.kwargs['pk'])
        return Question.objects.filter(pk=self.obj.pk)