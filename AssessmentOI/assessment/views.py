from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import *

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