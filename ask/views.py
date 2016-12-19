from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ask.forms import SignUpForm

# Create your views here.

questions = []
for i in xrange(1, 30):
    questions.append({
        'title': 'Title ' + str(i),
        'id': i,
        'text': 'test test test',
    })


def pagination(request, objects, objects_count, html_page):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')
    
    try:
        list_objects = paginator.page(page)
    except PageNotAnInteger:
        list_objects = paginator.page(1)
    except EmptyPage:
        list_objects = paginator.page(paginator.num_pages)
        
    return render_to_response(html_page, {'objects': list_objects})


def main_page(request):
    return pagination(request, questions, 5, 'questions.html')


def sign_in_page(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return render(request, 'sign_in.html')


def sign_up_page(request):
    if request.method == 'POST':
        form = SignUpForm()
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            return redirect('/')
        else:
            return render(request, 'sign_up.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def ask_page(request):
    return render_to_response('ask.html')


def answer_page(request):
    return render_to_response('answer.html')


def settings_page(request):
    return render_to_response('settings.html')