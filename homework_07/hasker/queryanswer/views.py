from django.shortcuts import render
from django.views.generic import ListView
from queryanswer.models import Query
# Create your views here.

class QueryesListView(ListView):
    model = Query
    template_name = 'queryanswer/index.html'
    context_object_name = 'queryes'
