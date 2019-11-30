from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBadRequest
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Question, Vote
from .forms import QuestionForm, AnswerForm
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from .forms import VoteForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class QuestionsListView(ListView):
    template_name = 'queryanswer/index.html'
    context_object_name = 'questions'
    paginate_by = 20
    model = Question


class HotQuestionsListView(ListView):
    template_name = 'queryanswer/index.html'
    # queryset = Question.objects.hot_question()


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                question=self.object,
                user=self.request.user
            )
            if vote.id:
                vote_form_url = reverse(
                    'queryanswer:UpdateVote',
                    kwargs = {
                        'question_id': vote.question.id,
                        'pk': vote.id
                    }
                )
            else:
                vote_form_url = (
                    reverse(
                        'queryanswer:CreateVote',
                        kwargs={
                            'question_id': self.object.id
                        }
                    )
                )
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url

        return ctx


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['question'] = self.kwargs['question_id']
        return initial

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse(
            'queryanswer:question',
            kwargs = {
                'pk': question_id})

    def render_to_response(self, context, **response_kwargs):
        question_id = context['object'].id
        print(question_id)
        question_detail_url = reverse(
            'queryanswer:question',
            kwargs= {'pk': question_id})
        return redirect(to=question_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied(
                'can not change another users vote')
        return vote

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse(
            'queryanswer:question',
            kwargs={
                'pk': question_id})

    def render_to_response(self, context, **response_kwargs):
        question_id = context['object'].id
        question_detail_url = reverse(
            'queryanswer:question',
            kwargs={
                'pk': question_id})
        return redirect(to=question_detail_url)
