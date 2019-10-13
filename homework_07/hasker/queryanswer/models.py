from django.db import models
from django.urls.base import reverse
from django.conf import settings


class Question(models.Model):
    slug = models.SlugField('Url', max_length=150, unique=True)
    title = models.CharField('Заголовок ', default='', max_length=120)
    body = models.TextField('Содержание')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Автор: ', on_delete=models.CASCADE)
    created = models.DateTimeField('Создано', auto_now_add=True)
    tags = models.CharField('Теги', max_length=50)

    class Meta:
        db_table = 'question'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('queryanswer:question', kwargs={'pk': self.id})

    def can_accept_answer(self, user):
        return user == self.user


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField('Ответ:', default='')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField('Создано:', auto_now_add=True)
    accept = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        db_table = 'answer'
    def __str__(self):
        return self.answer


class Vote(models.Model):
    UP = 1
    DOWN = -1
    CHOICES  = (
        (UP, ">"),
        (DOWN, "<")
    )
    value = models.SmallIntegerField(choices=CHOICES)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return str(self.votes)


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, user, question):
        try:
            return Vote.objects.get(question=question, user=user)
        except Vote.DoesNotExict:
            return Vote(question=question, user=user)
