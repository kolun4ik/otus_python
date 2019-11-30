from .views import QuestionsListView, AskQuestionView, QuestionDetailView, CreateVote, UpdateVote
from django.urls import path


app_name = 'queryanswer'


urlpatterns = [
    path('', QuestionsListView.as_view(), name='index'),
    path('ask/', AskQuestionView.as_view(), name='ask'),
    # path('question/<slug:slug>', QuestionDetailView.as_view(), name='question'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question'),
    path('question/<int:question_id>/vote', CreateVote.as_view(), name='CreateVote'),
    path('question/<int:question_id>/vote/<int:pk>', UpdateVote.as_view(), name='UpdateVote')
]