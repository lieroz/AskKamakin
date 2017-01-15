from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.http import HttpResponseRedirect

from ask.forms import LoginForm, SignupForm, SettingsForm, QuestionForm, AnswerForm
from ask.models import Question
from ask.ajax_features import login_required_ajax


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

    return render(request, 'template_form.html', {
        'form': form,
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

    return render(request, 'template_form.html', {
        'form': form,
    })


@login_required_ajax
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


@login_required_ajax
def settings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = SettingsForm(request.user, request.POST)

        if form.is_valid():
            form.save()

    else:
        form = SettingsForm(request.user)

    return render(request, 'template_form.html', {
        'form': form,
    })


@login_required_ajax
def question_add_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = QuestionForm()

    return render(request, 'template_form.html', {
        'form': form,
    })


@login_required_ajax
def question_view(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.user, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = AnswerForm(initial={'question_id': question_id})

    return render(request, 'template_form.html', {
        'question': question,
        'is_preview': False,
        'form': form,
    })



def main_page(request):
    questions = Question.objects.all()
    return pagination(request, questions, 5, 'main_page.html')
