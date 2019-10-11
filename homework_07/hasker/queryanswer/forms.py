from django import forms
from django.contrib.auth import get_user_model
from queryanswer.models import Question, Vote


class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model = Question
        fields = ['title','body','tags','user']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['value', 'user', 'question']