import sys

from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, CreateView
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import openpyxl # to upload file
import datetime
from users.models import User

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
        assessment = Assessment.objects.filter(token=self.kwargs['token'])[0]
        pk = assessment.pk
        questions_selected = Question.objects.filter(assessment__pk=pk)
        context['questions_selected'] = questions_selected

        # total number of questions
        number_of_questions = questions_selected.count()
        context['number_of_questions'] = number_of_questions
        context['duration'] = assessment.time_to_complete
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
                return HttpResponseRedirect(reverse('test_home_view'))
                # reset to make the old app working (without candidate)
                # return HttpResponseRedirect(reverse('validate_token_view'))
        else:
            return HttpResponseRedirect(reverse('test_home_view'))
            # return HttpResponseRedirect(reverse('validate_token_view'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_list_pk = []
        query_list = Question.objects.all() #.values_list('pk')
        [query_list_pk.append(q.pk) for q in query_list]

        current = kwargs['object'].pk

        current_idx = query_list_pk.index(current)

        if current_idx >= len(query_list_pk) - 1:
            next = 1
            previous = query_list_pk[current_idx - 1]

        elif current_idx == 0:
            next = query_list_pk[current_idx + 1]
            previous = query_list_pk[len(query_list_pk)-1]
        else:
            next = query_list_pk[current_idx + 1]
            previous = query_list_pk[current_idx - 1]
        try:
            image = True
            Question.objects.filter(pk=current)[0].image.url

        except:
            image = False
        context['image'] = image
        context['next'] = next
        context['previous'] = previous

        return context

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

# **** **** **** **** **** ****

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):

        template_name = 'assessment/home.html'
        context_object_name = 'home_view'
        # fields = '__all__'

        def get(self, request, *args, **kwargs):
            if request.user.is_staff:
                return HttpResponseRedirect(reverse('dashboard_view'))
            else:
                return HttpResponseRedirect(reverse('candidate_home_view'))
            pass

# **** Director Classes

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    model = Assessment
    template_name = 'assessment/assessment.html'
    context_object_name = 'assessment_view'
    ordering = ['-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()

        context['tot_number_of_assessment'] = len(Assessment.objects.all())

        context['assessment_created_30_days'] = len(Assessment.objects.filter(date_creation__range=[
                            datetime.datetime.now() - datetime.timedelta(30),
                            datetime.datetime.now()]))


        context['assessment_completed'] = len(Assessment.objects.exclude(date_complete = None))
        context['assessment_completed_30_days'] = len(Assessment.objects.filter(date_creation__range=[
                                             datetime.datetime.now() - datetime.timedelta(30),
                                             datetime.datetime.now()]).exclude(date_complete = None))


        return context

@method_decorator(login_required, name='dispatch')
class AssessmentListView(ListView):
    model = Assessment
    template_name = 'assessment/director/assessment_list.html'
    context_object_name = 'assessment_list_view'
    ordering = ['-pk']

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
        assessment = Assessment.objects.filter(pk=self.object.pk)[0]
        context['assessment'] = assessment
        return context


@method_decorator(login_required, name='dispatch')
class AssessmentCreateView(ListView):
    model = Assessment
    template_name = 'assessment/director/assessment_create.html'
    context_object_name = 'assessment_create_view'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.exclude(practice_question = 'Yes')
        try:
            context['message'] = self.request.session['message']
        except:
            context['message'] = ''
        self.request.session['message'] = ''
        # context['number_of_column'] =

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        questions_selected = [out for out in request.POST if 'table_records' in out]
        questions_selected_number = [x.split("_")[2] for x in questions_selected ]

        try:
            if len(User.objects.filter(email=request.POST['candidate_email'])) == 0:
                use = User(name=request.POST['candidate_name'], email=request.POST['candidate_email'])
                use.set_password(request.POST['candidate_password'])
                use.save()
            else:
                # use = User.objects.get(email=request.POST['candidate_email'])
                # use.set_password(request.POST['candidate_password'])
                # use.save()
                pass
        except:
            # user already exist DO NOTHING
            pass

        try:
            newAssessment = Assessment(
                assessment_name = request.POST['test_name'],

                candidate_name =  request.POST['candidate_name'],
                candidate_surname = request.POST['candidate_surname'],
                candidate_email = request.POST['candidate_email'],

                token = request.POST['token'],

                creator_email = request.user.email,

                date_creation = datetime.datetime.now(),

                time_to_complete = request.POST['duration'],

            )
            newAssessment.save()

            newAssessment.questions_selected.add(*questions_selected_number)
            newAssessment.save()
            return HttpResponseRedirect(reverse('assessment_list_view'))
        except ValueError:
            request.session['message'] = 'Assessment NOT Saved - Make sure the name of the assessment and the Token have NOT been used before. Retry'
            return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    model = Question
    template_name = 'assessment/director/question_create.html'
    context_object_name = 'question_create_view'
    fields = '__all__'

    # ordering = ['-date_elaboration']
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data_dict = {}


        data_dict['number_of_answers'] = request.POST['number_of_answers']
        data_dict['question'] = request.POST['question']
        if request.POST['radio'] == 'single':
            data_dict['question_type'] = 'Single Selection'
            data_dict['number_of_selection'] = 1
            data_dict['answer_1'] = request.POST['answer_s_1']
            data_dict['answer_1_value'] = 'Yes' if ('answer_s_1_value' in request.POST) else 'No'
            data_dict['answer_2'] = request.POST['answer_s_2']
            data_dict['answer_2_value'] = 'Yes' if ('answer_s_2_value' in request.POST) else 'No'
            data_dict['answer_3'] = request.POST['answer_s_3']
            data_dict['answer_3_value'] = 'Yes' if ('answer_s_3_value' in request.POST) else 'No'
            data_dict['answer_4'] = request.POST['answer_s_4']
            data_dict['answer_4_value'] = 'Yes' if ('answer_s_4_value' in request.POST) else 'No'
            data_dict['answer_5'] = request.POST['answer_s_5']
            data_dict['answer_5_value'] = 'Yes' if ('answer_s_5_value' in request.POST) else 'No'
        elif request.POST['radio'] == 'multi':
            data_dict['question_type'] = 'Multi Selection'
            data_dict['number_of_selection'] = request.POST['number_of_answers_selected']
            data_dict['answer_1'] = request.POST['answer_m_1']
            data_dict['answer_1_value'] = 'Yes' if ('answer_m_1_value' in request.POST) else 'No'
            data_dict['answer_2'] = request.POST['answer_m_2']
            data_dict['answer_2_value'] = 'Yes' if ('answer_m_2_value' in request.POST) else 'No'
            data_dict['answer_3'] = request.POST['answer_m_3']
            data_dict['answer_3_value'] = 'Yes' if ('answer_m_3_value' in request.POST) else 'No'
            data_dict['answer_4'] = request.POST['answer_m_4']
            data_dict['answer_4_value'] = 'Yes' if ('answer_m_4_value' in request.POST) else 'No'
            data_dict['answer_5'] = request.POST['answer_m_5']
            data_dict['answer_5_value'] = 'Yes' if ('answer_m_5_value' in request.POST) else 'No'
        else:
            data_dict['question_type'] = 'Essay'

        data_dict['answers'] = 'Test'

        model = 'Question'
        table_name = model
        model_class = getattr(sys.modules[__name__], table_name)

        try:
            model_class(**data_dict).save()
            print('question saved')
        except:
            print('question not saved')

        return HttpResponseRedirect(reverse('question_list_view'))

@method_decorator(login_required, name='dispatch')
class QuestionCreateFromFileView(CreateView):
    model = Question
    template_name = 'assessment/director/question_create.html'
    context_object_name = 'question_upload_from_file'
    fields = '__all__'

    # ordering = ['-date_elaboration']
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        saved_questions = []
        not_saved_questions = []
        if (len(request.FILES)!=0) :
            excel_file = request.FILES["myfile"]
            model = 'Question'

            wb = openpyxl.load_workbook(excel_file)

            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)
            # self.form_class.CHOICES

            excel_data = list()
            excel_data_no_headers = list()
            # iterating over the rows and
            # getting value from each cell in row

            table_name = model
            model_class = getattr(sys.modules[__name__], table_name)
            i = 0 #i represent the rows
            headers_file = []
            data_dict = {}
            data_dict_rows= {}
            for row in worksheet.iter_rows():
                row_data = list()
                j = 0
                for cell in row:
                    if cell.value:
                        row_data.append(str(cell.value))
                        if i != 0:
                            data_dict[headers_file[j]] = str(cell.value)
                    else:
                        row_data.append(None)
                        if i != 0:
                            data_dict[headers_file[j]] = None

                    j = j + 1
                if i != 0:
                    data_dict_rows['row_' + str(i)] = data_dict

                if i == 0:
                    headers_file = row_data

                else:
                    try:
                        excel_data_no_headers.append(row_data)
                        model_class(**data_dict).save()
                        print('saved question number:%s'% i)
                        saved_questions.append(i)
                    except:
                        print('not saved')
                        not_saved_questions.append(i)
                        pass
                data_dict = {}
                excel_data.append(row_data)
                i = i + 1

            self.request.session['headers_file'] = headers_file
            self.request.session['excel_data'] = excel_data
            self.request.session['excel_data_no_headers'] = excel_data_no_headers
            self.request.session['data_dict_rows'] = data_dict_rows
            self.request.session['model'] = model # the uploaded table
            self.request.session['upload'] = 'loaded' # table created from file

            self.request.session['saved_questions'] = saved_questions
            self.request.session['not_saved_questions'] = not_saved_questions

            return HttpResponseRedirect(reverse('question_uploaded_view'))
            # return super().post(request, *args, **kwargs)
        else:

            return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class QuestionUploadedView(TemplateView):

    def get_context_data(self, **kwargs):
        # token = self.kwargs['token']
        context = super().get_context_data(**kwargs)
        context['saved_questions'] = self.request.session['saved_questions']
        context['not_saved_questions'] = self.request.session['not_saved_questions']

        return context

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'assessment/directo/question_list.html'
    context_object_name = 'question_list_view'
    ordering = ['-pk']

    # ordering = ['-date_elaboration']
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context







# **** Candidate Classes

@method_decorator(login_required, name='dispatch')
class CandidateHomeView(TemplateView):

        template_name = 'assessment/home.html'
        context_object_name = 'candidate_home_view'

        def get_context_data(self, **kwargs):
            # token = self.kwargs['token']
            context = super().get_context_data(**kwargs)
            try:
                context['assessment'] = Assessment.objects.filter(candidate_email__iexact=self.request.user.email)[0]
            except:
                context['assessment'] = []
            return context

        def get(self, request, *args, **kwargs):

            return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PracticeQuestionsView(TemplateView):
    model = Assessment
    template_name = 'assessment/test_questions.html'
    context_object_name = 'test_questions_view'
    # slug_field = 'token'
    # slug_url_kwarg = 'token'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['assessment'] = Assessment.objects.filter(assessment=self.kwargs['pk'])
        try:
            pk = Assessment.objects.filter(token='Practice_Test')[0].pk
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
        except:
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
class TestHomeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        return context

    def get(self, request, *args, **kwargs):
        email_user = request.user.email
        try:
            query_assessment = Assessment.objects.filter(candidate_email__iexact=email_user)[0]
        except:
            return super().get(request, *args, **kwargs)

        if query_assessment.completed == 'No':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home_view'))
    def post(self,request, *args, **kwargs):

        email_user = request.user.email
        token = request.POST['token']
        # 'Practice_Test' the token has to be different from this
        # TODO: check also if the test has already been taken
        query_assessment = Assessment.objects.filter(token=token,candidate_email=email_user) #the token is unique do it will return one single value
        if query_assessment.exists():
            if query_assessment[0].candidate_email.lower() == email_user.lower():
                if query_assessment[0].completed == 'No':
                    return HttpResponseRedirect(reverse('test_token_validated_view',kwargs={'token':token}))
                else:
                    kwargs['message'] = 'Assessment Completed'
                    return HttpResponseRedirect(reverse('home_view'))
        else:
            kwargs['message'] = 'Invalid Token'
            return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TestTokenValidatedView(TemplateView):
    model = Assessment
    template_name = 'assessment/test_token_validated.html'
    context_object_name = 'test_token_validated_view'
    # slug_field = 'token'
    # slug_url_kwarg = 'token'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # object = Assessment.objects.get(candidate_email=self.request.user.email, token=token)
        assess = Assessment.objects.filter(candidate_email=self.request.user.email, token=kwargs['token'])[0]
        context['object'] = assess

        context['time_to_complete'] = assess.time_to_complete
        context['number_of_questions'] = len(Question.objects.filter(assessment__pk = assess.pk))

        return context

    def post(self,request, *args, **kwargs):
        # token = self.kwargs['token']
        # return HttpResponseRedirect(reverse('home_view', kwargs={'token': token}))

        return self.get(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        token = self.kwargs['token']
        # return HttpResponseRedirect(reverse('home_view', kwargs={'token': token}))
        object = Assessment.objects.get(candidate_email=self.request.user.email,token=token)

        object.date_first_opened = datetime.datetime.now()
        object.save()


        return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TestCandidateQuestionsView(TemplateView):
    model = Assessment
    template_name = 'assessment/candidate/test_questions.html'
    context_object_name = 'test_questions_view'
    # slug_field = 'token'
    # slug_url_kwarg = 'token'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email_user = self.request.user.email
        # context['assessment'] = Assessment.objects.filter(assessment=self.kwargs['pk'])
        assessment = Assessment.objects.filter(token=self.kwargs['token'],candidate_email=email_user)[0]
        pk = assessment.pk
        questions_selected = Question.objects.filter(assessment__pk=pk)
        context['questions_selected'] = questions_selected

        # total number of questions
        number_of_questions = questions_selected.count()
        context['number_of_questions'] = number_of_questions

        context['duration'] = assessment.time_to_complete
        context['object'] = assessment
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
        email_user = request.user.email
        # token = request.POST['token']

        # query token and user to see if the candidate has an assessment assigned

        # test if it exist pass user and token (the token is unique... but we want to verify the correct email too)
        assessment_query = Assessment.objects.filter(token=token,candidate_email=email_user)
        if assessment_query:
            assessment = Assessment.objects.filter(token=token,candidate_email=email_user)[0]
            if assessment.candidate_email.lower() == request.user.email.lower():
                if assessment.completed == 'Yes':

                    # return HttpResponseRedirect(reverse('home_view',kwargs = {'token': token}))
                    return HttpResponseRedirect(reverse('home_view'))

                else:
                    return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('test_home_view'))
                # reset to make the old app working (without candidate)
                # return HttpResponseRedirect(reverse('validate_token_view'))
        else:
            return HttpResponseRedirect(reverse('test_home_view'))
            # return HttpResponseRedirect(reverse('validate_token_view'))

        # check if the token and the user are valid at the same time.


@method_decorator(login_required, name='dispatch')
class TestQuestionsSubmitUpdate(TemplateView):
    model = Assessment
    template_name = 'assessment/test_questions_submit.html'
    context_object_name = 'test_questions_submit_view'
    # fields = '__all__'
    # form_class = AssessmentForm
    # slug_field = 'token'
    # slug_url_kwarg = 'token'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment'] = Assessment.objects.filter(token=self.kwargs['token'],candidate_email=self.request.user.email)[0]

        return context

    def post(self, request, *args, **kwargs):
        token = self.kwargs['token']
        test = Assessment.objects.filter(token=token,candidate_email=self.request.user.email)[0]
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
            test.date_complete = datetime.datetime.now()
            test.completed = 'Yes'
            test.answers = answers
            test.save()

        return HttpResponseRedirect(reverse('test_questions_submit_view',kwargs = {'token': token}))

    def calculate_score(self,assessment,answers):
        pass
    pass

# @method_decorator(login_required, name='dispatch')
# class TestQuestionsSubmitUpdate(UpdateView):
#     model = Assessment
#     template_name = 'assessment/test_questions_submit.html'
#     context_object_name = 'test_questions_submit_view'
#     # fields = '__all__'
#     form_class = AssessmentForm
#     slug_field = 'token'
#     slug_url_kwarg = 'token'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['assessment'] = Assessment.objects.filter(token=self.kwargs['token'])[0]
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         token = self.kwargs['token']
#         test = Assessment.objects.filter(token=token)[0]
#         # [values.append(value) for value in request.POST]
#         answers = {}
#         for element in request.POST.items():
#             answer_list = []
#             if element[0].startswith('Q'):
#                 if "-" in element[0]:
#                     question_number = element[0].split('-')[0]
#                     answer_number = element[1]
#                     answer_list.append(answer_number)
#                     # check if the question already exist and hence is a multiple choice
#                     if question_number in answers:
#                         answers[question_number].append(answer_number)
#                     else:
#                         answers[question_number] = answer_list
#                 else:
#                     question_number = element[0]
#                     answer_number = element[1]
#                     answer_list.append(answer_number)
#                     answers[question_number]= answer_list
#                     pass
#         # we should test if it comes from a valid form (it maybe access directly from the URL?)
#
#         # Register information, answers and result
#         if test.completed != 'Yes':
#             test.date_complete = datetime.now()
#             test.completed = 'Yes'
#             test.answers = answers
#             test.save()
#
#         return HttpResponseRedirect(reverse('test_questions_submit_view',kwargs = {'token': token}))
#
#     def calculate_score(self,assessment,answers):
#         pass
#     pass
@method_decorator(login_required, name='dispatch')
class AssessementCopyView(CreateView):
    model = Assessment
    template_name = 'assessment/director/assessment_copy.html'
    context_object_name = 'assessment_copy_view'



    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        assessment = Assessment.objects.get(pk=pk)
        assessment_name = assessment.assessment_name

# **************** routine to add '_1' to the name and email before creating a new assessment and new user

        if assessment_name[len(assessment_name)-1].isnumeric():
                if assessment_name[len(assessment_name)-2] == '_':
                    assessment_name = assessment_name[:len(assessment_name)-2] + '_' + str(int(assessment_name[len(assessment_name)-1]) + 1)
                else:
                    assessment_name = assessment_name + '_1'
        else:
            assessment_name = assessment_name + '_1'

        candidate_email = assessment.candidate_email

        candidate_email_no_at = candidate_email.split('@')[0]

        if candidate_email_no_at[len(candidate_email_no_at)-1].isnumeric():
                if candidate_email_no_at[len(candidate_email_no_at)-2] == '_':
                    candidate_email_no_at = candidate_email_no_at[:len(candidate_email_no_at)-2] + '_' + str(int(candidate_email_no_at[len(candidate_email_no_at)-1]) + 1)
                else:
                    candidate_email_no_at = candidate_email_no_at + '_1'
        else:
            candidate_email_no_at = candidate_email_no_at + '_1'

        candidate_email = candidate_email_no_at +'@'+candidate_email.split('@')[1]

        if len(User.objects.filter(email=candidate_email)) != 0 :
            candidate_email = candidate_email.split('@')[0]+'_1@'+candidate_email.split('@')[1]

        if len(Assessment.objects.filter(assessment_name=assessment_name)) != 0:
            assessment_name = assessment_name + '_1'



        try:

            newUser = User(name=assessment.candidate_name,email=candidate_email)
            newUser.save()
            newUser.set_password('OracleInsightforCloud')
            newUser.save()
            newAssessment = Assessment(
                assessment_name=assessment_name,
                candidate_name=assessment.candidate_name,
                candidate_surname=assessment.candidate_surname,
                candidate_email=candidate_email,
                time_to_complete =assessment.time_to_complete,
                creator_email = assessment.creator_email,
                date_creation=datetime.datetime.now(),
                # questions_selected = assessment.questions_selected,
                token=assessment.token,
            )
            # newAssessment.questions_selected.set(assessment.questions_selected)
            questions_selected_number = []
            questions_selected = Question.objects.filter(assessment__pk=assessment.pk)

            [questions_selected_number.append(q.pk) for q in questions_selected]
            newAssessment.save()
            newAssessment.questions_selected.add(*questions_selected_number)
            newAssessment.save()

            return HttpResponseRedirect(reverse('assessment_list_view'))

        except:
            return HttpResponseRedirect(reverse('assessment_list_view'))

    def post(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)
        pass

