from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Question(models.Model):

    class Meta:
        db_table = "question"

    question_title = models.CharField(max_length=255)
    question_text = models.TextField()
    question_date = models.DateTimeField()
    question_likes = models.IntegerField(default=0)


class Comments(models.Model):

    class Meta:
        db_table = "comments"

    comments_text = models.TextField()
    comments_question = models.ForeignKey(Question)