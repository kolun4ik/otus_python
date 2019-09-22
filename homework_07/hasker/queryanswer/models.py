from django.db import models
from django.urls.base import reverse
from django.conf import settings


class Question(models.Model):
    title = models.CharField('Заголовок ', default='', max_length=120)
    body = models.TextField('Содержание: ')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Автор: ', on_delete=models.CASCADE)
    created = models.DateTimeField('Создано: ', auto_now_add=True)
    tags = models.CharField('Теги', max_length=50)

    class Meta:
        db_table = 'question'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:question', kwargs={'pk': self.id})

    def can_accept_answer(self, user):
        return user == self.user


class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    answer = models.TextField('Ответ:', default='')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField('Создано:', auto_now_add=True)
    accept = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        db_table = 'answer'
