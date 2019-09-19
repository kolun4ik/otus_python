from django.db import models
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Question(models.Model):
    title = models.CharField('Заголовок: ', default='', max_length=120)
    body = models.TextField('Содержание: ')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Автор: ', on_delete=models.CASCADE)
    created = models.DateTimeField('Создано: ', auto_now_add=True)
    tags = models.CharField('Теги', max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:questions_detail', kwargs={'pk': self.id})

    def can_accept_answer(self, user):
        return user == self.user

class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    body = models.TextField('Ответ:', default='')
    autor = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField('Создано:', auto_now_add=True)
    accept = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
