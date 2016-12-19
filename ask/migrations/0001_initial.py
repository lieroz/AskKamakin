# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-18 18:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_body', models.TextField()),
                ('answer_date', models.DateTimeField()),
                ('answer_rating', models.IntegerField(default=0)),
                ('answer_is_correct', models.BooleanField(default=False)),
                ('answer_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField()),
                ('comment_date', models.DateTimeField()),
                ('comment_rating', models.IntegerField(default=0)),
                ('comment_likes', models.IntegerField(default=0)),
                ('comment_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Answer')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'like',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=30)),
                ('question_body', models.TextField()),
                ('question_date', models.DateTimeField()),
                ('question_rating', models.IntegerField(default=0)),
                ('question_likes', models.IntegerField(default=0)),
                ('question_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question',
            },
            managers=[
                ('questions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to=b'avatars')),
                ('info', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Question'),
        ),
    ]
