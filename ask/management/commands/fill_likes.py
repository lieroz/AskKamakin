from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ask.models import Question, QuestionLike, Answer, AnswerLike
from random import choice


class Command(BaseCommand):
    help = 'Fill likes'

    def add_arguments(self, parser):
        parser.add_argument('--number-answers',
                            action='store',
                            dest='number_answers',
                            default=5,
                            help='Number of likes for an answer'
                            )
        parser.add_argument('--number-questions',
                            action='store',
                            dest='number_questions',
                            default=5,
                            help='Number of likes for a question'
                            )

    def handle(self, *args, **options):
        number_of_answers = int(options['number_answers'])
        number_of_questions = int(options['number_questions'])

        users = User.objects.all()[1:]
        questions = Question.objects.all()

        for question in questions:
            self.stdout.write('question [%d]' % question.id)

            for i in range(number_of_questions):
                QuestionLike.objects.add_or_update(
                    author=choice(users),
                    question=question,
                    value=choice([-1, 1])
                )

        answers = Answer.objects.all()

        for answer in answers:
            self.stdout.write('answer [%d]' % answer.id)

            for i in range(number_of_answers):
                AnswerLike.objects.add_or_update(
                    author=choice(users),
                    answer=answer,
                    value=choice([-1, 1])
                )
