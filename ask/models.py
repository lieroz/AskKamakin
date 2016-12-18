from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
import datetime
import random


class Comment(models.Model):
    class Meta:
        db_table = "comment"

    comment_author = models.ForeignKey(User)
    comment_body = models.TextField()
    comment_date = models.DateTimeField()
    comment_rating = models.IntegerField(default=0)
    comment_answer = models.ForeignKey(Answer)

    def get_url(self):
        return self.comment_question.get_url()


class Answer(models.Model):
    class Meta:
        db_table = "answer"

    answer_author = models.ForeignKey(User)
    answer_body = models.TextField()
    answer_date = models.DateTimeField()
    answer_rating = models.IntegerField(default=0)
    answer_is_correct = models.BooleanField(default=False)
    answer_question = models.ForeignKey(Question)

    def get_comments(self):
        return Comment.objects.filter(comment_answer_id=self.id)

    def get_url(self):
        return self.answer_question.get_url()


class Question(models.Model):
    class Meta:
        db_table = "question"

    question_title = models.CharField(max_length=30)
    question_body = models.TextField()
    question_date = models.DateTimeField()
    question_rating = models.IntegerField(default=0)
    question_author = models.ForeignKey(User)

    def get_answers(self):
        return Answer.objects.filter(answer_question_id=self.id)

    def get_url(self):
        return '/question{question_id}/'.format(question_id=self.id)


class Tag(models.Model):



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()


class Like(models.Model):

