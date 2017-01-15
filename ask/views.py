from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect, Http404

from ask.forms import LoginForm, SignupForm, SettingsForm
from ask.models import Question, Answer, Tag


def pagination(request, objects, objects_count, html_page):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        list_objects = paginator.page(page)
    except PageNotAnInteger:
        list_objects = paginator.page(1)
    except EmptyPage:
        list_objects = paginator.page(paginator.num_pages)

    return render(request, html_page, {'objects': list_objects})


def new(request, page):
    questions_query = Question.objects.list_new()
    questions = pagination(request, questions_query, 4)

    return render(request, 'index.html', {'questions': questions})


def hot(request, page):
    questions_query = Question.objects.list_new()
    questions = pagination(request, questions_query, 4)

    return render(request, 'hot.html', {'questions': questions})


def answer(request, id):
    try:
        answer = Answer.objects.get(id=id)
    except Answer.DoesNotExist:
        raise Http404()

    return render(request, 'answer.html', {'answer': answer})


def tag(request, htag, page):
    context = RequestContext(request, {
        'hash_tag': htag,
    })

    try:
        tag = Tag.objects.get_by_title(htag)
    except Tag.DoesNotExist:
        raise Http404()

    questions_query = Question.objects.list_tag(tag)
    questions = pagination(questions_query, request, 4)

    return render(request, 'tag.html', {'questions': questions, 'context': context})


def question(request, question_id):
    try:
        ques = Question.objects.get_single(int(question_id))
    except Question.DoesNotExist:
        raise Http404()

    return render(request, 'question.html', {'question': ques})


@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


def login(request):
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
        'form': form
    })


def signup(request):
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
    })


def main_page(request):
    questions = Question.objects.all()
    return pagination(request, questions, 5, 'main_page.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
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
    })