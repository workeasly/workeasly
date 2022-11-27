from django import forms
from .models import *


class AddNewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('user', 'title', 'details', 'is_active', 'completed', 'started', 'started_on', 'completed_on','id')
