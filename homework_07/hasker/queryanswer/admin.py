from django.contrib import admin
from .models import Question, Answer, Vote



class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created']

class AnswerAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)