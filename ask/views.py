from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

questions = []
for i in xrange(1, 30):
    questions.append({
        'title': 'Title ' + str(i),
        'id': i,
        'text': 'test test test',
    })

def pagination(request, objects, objects_count, html_page, name):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')
    
    try:
        list_objects = paginator.page(page)
    except PageNotAnInteger:
        list_objects = paginator.page(1)
    except EmptyPage:
        list_objects = paginator.page(paginator.num_pages)
        
    return render_to_response(html_page, {name: list_objects})

def main_page(request):
    return pagination(request, questions, 5, 'questions.html', 'questions')

def sign_in_page(request):
    return render_to_response('sign_in.html')

def sign_up_page(request):
    return render_to_response('sign_up.html')

def ask_page(request):
    return render_to_response('ask.html')

def answer_page(request):
    return render_to_response('answer.html')

def settings_page(request):
    return render_to_response('settings.html')