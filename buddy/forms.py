from django import forms
from .models import *

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = []
        fields = ['profilepic','bio','contact',]


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
        fields = ['first_name','last_name', 'email']


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        exclude = ['admin']


class RegGym(forms.ModelForm):
    class Meta:
        model = Gym
        exclude = ['owner']


class RunSession(forms.ModelForm):
    class Meta:
        model = Run
        exclude = ['profile']


class SquatSession(forms.ModelForm):
    class Meta:
        model = WeightLifting
        exclude = ['benchpress','deadlift','profile']


class BenchSession(forms.ModelForm):
    class Meta:
        model = WeightLifting
        exclude = ['squats','deadlift','profile']


class LiftSession(forms.ModelForm):
    class Meta:
        model = WeightLifting
        exclude = ['benchpress','squats','profile']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['chatroom','poster']

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['commentator','comment_post']