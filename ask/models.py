from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse


# Wrapper for User model to add new fields
class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='uploads')
    info = models.TextField()


# Manages methods and logic for Tag model
class TagManager(models.Manager):
    # Adds number of questions to each tag
    def with_questions_count(self):
        return self.annotate(questions_count=Count('question'))

    # Sorts tags by number of questions
    def order_by_question_count(self):
        return self.with_questions_count().order_by('-questions_count')

    # Searches tags using its title
    def get_by_title(self, title):
        return self.get(title=title)

    # Gets if tag exists else creates
    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(title=title)
        return tag

    # Counts popular questions in range
    def count_popular(self, amount):
        questions_count = Count('question')

        if amount > questions_count:
            amount = questions_count

        return self.order_by_question_count().all()[:questions_count]


# Describes Tag model
class Tag(models.Model):
    objects = TagManager()

    title = models.CharField(max_length=20)

    def get_url(self):
        return reverse(kwargs={'tag': self.title})


# Manages question methods and logic
class QuestionManager(models.Manager):
    # Lists all new questions
    def list_new(self):
        return self.order_by('-date')

    # Lists all hot questions
    def list_hot(self):
        return self.order_by('-likes')

    # Lists all questions with specific tag
    def list_tag(self, tag):
        return self.filter(tags=tag)


# Describes Question model
class Question(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()

    class Meta:
        db_table = 'question'
        ordering = ['-date']

    def get_url(self):
        return reverse('question', kwargs={'id': self.id})


# Manages likes for a question
class QuestionLikeManager(models.Manager):
    # Returns amount of likes for a question
    def sum_for_question(self, question):
        return self.filter(question=question).aggregate(sum=Sum('value'))['sum']

    # Adds like if doesn't exist
    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(
            author=author,
            question=question,
            defaults={'value': value}
        )

        question.likes = self.sum_for_question(question)
        question.save()

        return new


# Desribes QuestionLike model
class QuestionLike(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()


# Describes Answer model
class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'answer'
        ordering = ['-correct', 'date', '-likes']


# Manages likes for an answer
class AnswerLikeManager(models.Manager):
    # Returns amount of likes for an answer
    def sum_for_answer(self, answer):
        return self.filter(answer=answer).aggregate(sum=Sum('value'))['sum']

    # Adds like if doesn't exist
    def add_or_update(self, author, answer, value):
        obj, new = self.update_or_create(
            author=author,
            answer=answer,
            defaults={'value': value}
        )

        answer.likes = self.sum_for_answer(answer)
        answer.save()

        return new


# Desribes AnswerLike model
class AnswerLike(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()
