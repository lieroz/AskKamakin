from django.core.management.base import BaseCommand
from ask.models import Question, Tag
from random import choice


class Command(BaseCommand):
    help = 'Fill tags'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=3,
                            help='Number of tags for a question'
                            )

    def handle(self, *args, **options):
        tags = [
            'javascript', 'java', 'c#', 'php', 'android', 'jquery', 'python',
            'html', 'css', 'c++', 'ios', 'mysql', 'objective-c', 'sql', 'asp.net',
            'ruby-on-rails', 'iphone', 'angularjs', 'regexp'
        ]

        for tag in tags:

            if len(Tag.objects.filter(title=tag)) == 0:
                t = Tag()
                t.title = tag
                t.save()

        number = int(options['number'])
        tags = Tag.objects.all()

        for question in Question.objects.all():
            self.stdout.write('question [%d]' % question.id)

            if len(question.tags.all()) < number:

                for i in range(number - len(question.tags.all())):
                    t = choice(tags)

                    if t not in question.tags.all():
                        question.tags.add(t)
