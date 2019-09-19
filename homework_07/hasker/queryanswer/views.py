from django.shortcuts import render
from django.views.generic import ListView
from queryanswer.models import Question
# Create your views here.

class QueryesListView(ListView):
    model = Question
    template_name = 'queryanswer/index.html'
    context_object_name = 'questions'
