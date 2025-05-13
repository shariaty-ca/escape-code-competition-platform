from django import forms
from .models import Participant, Competition
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CompetitionRegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['team_name']  # Add other fields as needed
        
    def __init__(self, *args, **kwargs):
        self.competition = kwargs.pop('competition', None)
        super().__init__(*args, **kwargs)