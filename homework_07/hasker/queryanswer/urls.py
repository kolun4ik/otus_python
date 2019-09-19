from queryanswer.views import QueryesListView
from django.urls import path


app_name = 'questions'


urlpatterns = [
    path('', QueryesListView.as_view(), name='index'),
]