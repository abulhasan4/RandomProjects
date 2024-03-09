from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_type', 'duration', 'intensity', 'description']

