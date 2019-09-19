from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm