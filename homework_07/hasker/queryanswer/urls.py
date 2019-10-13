from queryanswer.views import QuestionsListView, AskQuestionView, QuestionDetailView
from django.urls import path


app_name = 'queryanswer'


urlpatterns = [
    path('', QuestionsListView.as_view(), name='index'),
    path('ask/', AskQuestionView.as_view(), name='ask'),
    path('question/<slug:slug>', QuestionDetailView.as_view(), name='question')
]