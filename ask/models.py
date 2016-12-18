from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
import datetime

# Create your models here.


class QuestionManager(models.Manager):

    def list_new(self):
        return self.order_by('-date')

    def list_hot(self):
        return self.order_by('-likes')

    def list_tag(self, tag):
        return self.filter(tags=tag)


class Question(models.Model):

    class Meta:
        db_table = 'question'

    question_title = models.CharField(max_length=255)
    question_text = models.TextField()
    question_date = models.DateTimeField()
    question_likes = models.IntegerField(default=0)
    question_author = models.ForeignKey(User, default=0)

    objects = QuestionManager()


class Answer(models.Model):
  
    class Meta:
        db_table = 'answer'
        
    answer_author = models.ForeignKey(User, default=0)
    answer_text = models.TextField()
    answer_likes = models.IntegerField(default=0)
    answer_date = models.DateTimeField()
    
    
class Tag(models.Model):
    
    class Meta:
        db_table = 'tag'
        
    tag_name = models.CharField(max_length=20)
    

class Like(models.Model):
    
    class Meta:
        db_table = 'like'
        
    LIKE = 1
    DISLIKE = -1
    
    like_author = models.ForeignKey(User)
    like_value = models.IntegerField(default=1)
    

class Profile(models.Model):
    user = models.OneToOneField(User)
    

class Comments(models.Model):

    class Meta:
        db_table = 'comments'

    comments_text = models.TextField()
    comments_question = models.ForeignKey(Question)