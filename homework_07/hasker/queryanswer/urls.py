from queryanswer.views import QueryesListView, AskView
from django.urls import path


app_name = 'questions'


urlpatterns = [
    path('', QueryesListView.as_view(), name='index'),
    path('ask/', AskView.as_view(), name='ask'),
]