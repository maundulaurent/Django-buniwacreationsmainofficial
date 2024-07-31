# Portal/forms.py

from django import forms
from .models import *
from datetime import datetime


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['project_name', 'description']

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date', 'image']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'value': datetime.today().strftime('%Y-%m-%d')}),
        }

