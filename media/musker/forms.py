from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Meep, Profile
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Frist Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}))
    # password = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter password'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Any):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password must contain at least 8 characters.</li><li>Your password cannot be entirely numeric.</li><li>Your password cannot be too similar to your other personal information.</li><li>Your password must contain at least one uppercase letter, one lowercase letter, and one special character.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter Confirm password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password</small></span>'


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Picture')
    profile_bio = forms.CharField(label="Profile Bio", max_length=500, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Bio'})) 
    homepage_link = forms.CharField(label="Homepage-Link", max_length=500, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Home Link'}))
    facebook_link = forms.CharField(label="Facebook", max_length=500, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Facebook ID'}))
    instagram_link = forms.CharField(label="Instagram", max_length=500, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Instagram ID'}))
    linkedin_link = forms.CharField(label="Linkedin", max_length=500, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Linkedin Link'}))

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'linkedin_link', 'instagram_link', 'facebook_link',)

class MeepForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Enter Your TWITE !!....',
                'class':'form-control',
            }
        ),
        label="",
    )


    class Meta:
        model = Meep
        exclude = ("user", "likes",)
