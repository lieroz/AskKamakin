from django.contrib import admin
from models import *


class QuestionInline(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'date']
    inlines = [QuestionInline]
    list_filter = ['date', 'likes']


admin.site.register(Profile)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
