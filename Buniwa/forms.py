from django import forms
from .models import blogComment
from .models import TextEntry
from .models import UserDetails
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
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = UserDetails
        fields = ['additional_name', 'mobile_number', 'country', 'state_region', 'profile_photo']