from django.contrib import admin
from ask.models import *

# Register your models here.


class QuestionInline(admin.StackedInline):
    model = Comments
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_title', 'question_text', 'question_date']
    inlines = [QuestionInline]
    list_filter = ['question_date']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile)