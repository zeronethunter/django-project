from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile
from .models import Rating


class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateVoteForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['up_vote', 'down_vote', 'user', 'question', 'answer']
