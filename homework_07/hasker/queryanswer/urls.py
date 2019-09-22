from queryanswer.views import QuestionsListView, AskQuestionView, QuestionDetailView
from django.urls import path


app_name = 'questions'


urlpatterns = [
    path('', QuestionsListView.as_view(), name='index'),
    path('ask/', AskQuestionView.as_view(), name='ask'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question')
]