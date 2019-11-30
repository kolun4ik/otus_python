from django import forms
from django.contrib.auth import get_user_model
from .models import Question, Answer, Vote


class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model = Question
        fields = ['slug', 'title', 'body', 'tags','user']

class AnswerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model=Answer
        fields = ['answer', ]

class VoteForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )
    question = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Question.objects.all(),
        disabled=True
    )

    value = forms.ChoiceField(
        label="Vote",
        widget=forms.RadioSelect,
        choices=Vote.CHOICES
    )

    class Meta:
        model = Vote
        fields = ['value', 'user', 'question']