from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def list_new(self):
        return self.order_by('-question_date')

    def list_popular(self):
        return self.order_by('-question_likes')


class Question(models.Model):
    class Meta:
        db_table = "question"

    question_title = models.CharField(max_length=30)
    question_body = models.TextField()
    question_date = models.DateTimeField()
    question_rating = models.IntegerField(default=0)
    question_author = models.ForeignKey(User)
    question_likes = models.IntegerField(default=0)

    questions = QuestionManager()

    def get_answers(self):
        return Answer.objects.filter(answer_question_id=self.id)

    def get_url(self):
        return '/question{question_id}/'.format(question_id=self.id)


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


class Comment(models.Model):
    class Meta:
        db_table = "comment"

    comment_author = models.ForeignKey(User)
    comment_body = models.TextField()
    comment_date = models.DateTimeField()
    comment_rating = models.IntegerField(default=0)
    comment_answer = models.ForeignKey(Answer)
    comment_likes = models.IntegerField(default=0)

    def get_url(self):
        return self.comment_question.get_url()


class Tag(models.Model):
    class Meta:
        db_table = "tag"

    tag_name = models.CharField(max_length=20)

    def get_questions(self):
        return Question.filter('tag')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()


class Like(models.Model):
    class Meta:
        db_table = "like"

    UP = 1
    DOWN = -1

    value = models.IntegerField(default=0)

