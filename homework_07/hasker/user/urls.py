from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from user.views import RegisterView, SettingsView

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('singup', RegisterView.as_view(), name='register'),
    path('settings', SettingsView.as_view(), name='settings'),
]
