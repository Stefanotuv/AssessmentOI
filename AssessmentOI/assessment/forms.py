from django import forms
from django.apps import apps
from .models import *
from django.forms import ClearableFileInput
# from django.utils.translation import ugettext_lazy as _


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'