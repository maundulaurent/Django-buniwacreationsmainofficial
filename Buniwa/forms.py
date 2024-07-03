from django import forms
from .models import blogComment
from .models import TextEntry
from django.contrib.auth.models import User



class blogCommentForm(forms.ModelForm):
    class Meta:
        model = blogComment
        fields = ['body']


class TexTEntryForm(forms.ModelForm):
    class Meta:
        model = TextEntry
        fields = ['text']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
