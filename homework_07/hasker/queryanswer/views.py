from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBadRequest
from django.views.generic import ListView, CreateView, DetailView
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.views.generic import FormView
from django.views.generic.edit import FormMixin


class QuestionsListView(ListView):
    template_name = 'queryanswer/index.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        return Question.objects.all().order_by('-created')


class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'queryanswer/ask.html'

    def get_initial(self):
        return {
            'user': self.request.user.id,
        }

    def form_valid(self, form):
       return super().form_valid(form)


class QuestionDetailView(DetailView, FormMixin):
    model = Question
    template_name = 'queryanswer/question.html'
    form_class = AnswerForm

