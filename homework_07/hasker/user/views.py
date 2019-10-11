from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.views.generic import UpdateView
from django.views.generic.edit import ModelFormMixin

# Create your views here.
class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm


class SettingsView(UpdateView, ModelFormMixin):
    template_name = 'user/settings.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user