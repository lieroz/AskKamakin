from django.contrib import admin
from models import *


class QuestionInline(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_title', 'question_body', 'question_date']
    inlines = [QuestionInline]
    list_filter = ['question_date', 'question_rating']


class AnswerInline(admin.StackedInline):
    model = Comment
    extra = 1


class AnswerAdmin(admin.ModelAdmin):
    fields = ['answer_date', 'answer_body']
    inlines = [AnswerInline]
    list_filter = ['answer_date', 'answer_rating']


admin.site.register(UserProfile)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionLike)
