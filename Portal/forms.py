# Portal/forms.py

from django import forms
from .models import ProjectRequest, Message


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['project_name', 'description']

class MilestoneForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }