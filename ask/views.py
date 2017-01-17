from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.http import HttpResponseRedirect

from ask.forms import LoginForm, SignupForm, SettingsForm, QuestionForm, AnswerForm
from ask.models import Question, Tag
from ask.ajax_features import login_required_ajax


def tags_decorator(func):
    def decorator(request, *args, **kwargs):
        tags = Tag.objects.count_popular()

        return func(request, tags=tags, *args, **kwargs)

    return decorator


@tags_decorator
def pagination(request, objects, objects_count, html_page, **kwargs):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        list_objects = paginator.page(page)
    except PageNotAnInteger:
        list_objects = paginator.page(1)
    except EmptyPage:
        list_objects = paginator.page(paginator.num_pages)

    return render(request, html_page, {
        'objects': list_objects,
        'tags': kwargs['tags'],
    })


@tags_decorator
def login(request, **kwargs):
    redirect = request.GET.get('continue', '/')

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])

            return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'tags': kwargs['tags'],
    })


@tags_decorator
def signup(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form,
        'tags': kwargs['tags'],
    })


@login_required_ajax
def logout(request, **kwargs):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


@tags_decorator
@login_required_ajax
def settings(request, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = SettingsForm(request.user, request.POST)

        if form.is_valid():
            form.save()

    else:
        form = SettingsForm(request.user)

    return render(request, 'settings.html', {
        'form': form,
        'tags': kwargs['tags'],
    })


@tags_decorator
@login_required_ajax
def question_add_form(request, **kwargs):
    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = QuestionForm()

    return render(request, 'ask.html', {
        'form': form,
        'tags': kwargs['tags'],
    })


@tags_decorator
@login_required_ajax
def single_question(request, question_id, **kwargs):
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.user, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = AnswerForm(initial={'question_id': question_id})

    return render(request, 'question.html', {
        'question': question,
        'is_preview': False,
        'form': form,
        'tags': kwargs['tags'],
    })


def main_page(request):
    questions = Question.objects.all()
    return pagination(request, questions, 5, 'base.html')
