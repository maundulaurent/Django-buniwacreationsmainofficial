from django import forms
from .models import blogComment
from .models import TextEntry
from .models import UserDetails
from django.contrib.auth.models import User
from PIL import Image


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
    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            img = Image.open(profile_photo)
            if img.size != (590, 560):
                # Add an error message to the form's profile_photo field
                raise forms.ValidationError("The profile photo must be 590x560 pixels. Please choose a different image.")
            
            elif img.size <= (250, 280):
                raise forms.ValidationError("The Profile Photo should be larger than 250x280. Please Select a different one")
        return profile_photo