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
    comment_is_correct = models.BooleanField(default=False)
    comment_rating = models.IntegerField(default=0)
    comment_question = models.ForeignKey(Question)

    def get_url(self):
        return self.comment_question.get_url()


class Question(models.Model):
    class Meta:
        db_table = "question"

    question_title = models.CharField(max_length=30)
    question_body = models.TextField()
    question_date = models.DateTimeField()
    question_rating = models.IntegerField(default=0)
    question_author = models.ForeignKey(User)

    def get_comments(self):
        return Comment.objects.filter(comment_question_id=self.id)

    def get_url(self):
        return '/question{question_id}/'.format(question_id=self.id)


class Answer(models.Model):


class Tag(models.Model):



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()


class Like(models.Model):

