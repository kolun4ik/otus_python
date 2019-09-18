from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Query(models.Model):
    title = models.CharField('Заголовок: ', default='', max_length=120)
    body = models.TextField('Содержание: ')
    author = models.ForeignKey(to=User, verbose_name='Автор: ', on_delete=models.CASCADE)
    created = models.DateTimeField('Создано: ', auto_now_add=True)
    tags = models.CharField('Теги', max_length=50)

    def __str__(self):
        return self.title