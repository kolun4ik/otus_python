from django.db import models
from django.urls.base import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models.aggregates import Sum
import math


class HotQuestionManger(models.Manager):
    """Hot Question Manager"""
    def get_queryset(self):
        pass

    def hot_question(self):
        qs = self.get_queryset()
        qs = qs.annotate(
            vote_sum=Sum('vote_value')
        )
        qs = qs.exclude(
            vote_sum=None
        )
        qs = qs.order_by('-vote_sum')
        return qs

class Question(models.Model):
    slug = models.SlugField('Url', max_length=150, unique=True)
    title = models.CharField('Заголовок ', default='', max_length=120)
    body = models.TextField('Содержание')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Автор: ', on_delete=models.CASCADE)
    created = models.DateTimeField('Создано', auto_now_add=True)
    tags = models.CharField('Теги', max_length=50)

    objects = models.Manager()

    class Meta:
        db_table = 'question'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('queryanswer:question', kwargs={'pk': self.id})

    def can_accept_answer(self, user):
        return user == self.user

    def timeago(self):
        now = timezone.now()
        timediff = now - self.created
        if timediff.days == 0 and timediff.seconds >= 0 and timediff.seconds < 60:
            seconds = timediff.seconds
            if seconds == 1:
                return "asked " + str(seconds) + "second ago"
            else:
                return "asked " + str(seconds) + "seconds ago"
        
        if timediff.days == 0 and timediff.seconds >= 60 and timediff.seconds < 3600:
            minutes = math.floor(timediff.seconds / 60)

            if minutes == 1:
                return "asked " + str(minutes) + " minute ago"

            else:
                return "asked " + str(minutes) + " minutes ago"

        if timediff.days == 0 and timediff.seconds >= 3600 and timediff.seconds < 86400:
            hours = math.floor(timediff.seconds / 3600)

            if hours == 1:
                return "asked " + str(hours) + " hour ago"

            else:
                return "asked " + str(hours) + " hours ago"

            # 1 day to 30 days
        if timediff.days >= 1 and timediff.days < 30:
            days = timediff.days

            if days == 1:
                return "asked " + str(days) + " day ago"

            else:
                return "asked " + str(days) + " days ago"

        if timediff.days >= 30 and timediff.days < 365:
            months = math.floor(timediff.days / 30)

            if months == 1:
                return "asked " + str(months) + " month ago"

            else:
                return "asked " + str(months) + " months ago"

        if timediff.days >= 365:
            years = math.floor(timediff.days / 365)

            if years == 1:
                return "asked " + str(years) + " year ago"

            else:
                return "asked " + str(years) + " years ago"


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


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, question, user):
        try:
            return Vote.objects.get(
                question=question,
                user=user)
        except Vote.DoesNotExist:
            return Vote(
                question=question,
                user=user)


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
    # votes = models.IntegerField(default=0)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return str(self.value)



