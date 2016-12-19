from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sign_in/', views.sign_in_page, name='sign_in_page'),
    url(r'^sign_up/', views.sign_up_page, name='sign_up_page'),
    # url(r'^question(?P<question_id>\d+)/', views.question, name='question'),
    # url(r'^questions(?P<page>\d+)/', views.question_page),
    url(r'^ask/', views.ask_page, name='ask_page'),
    url(r'^answer/', views.answer_page, name='answer_page'),
    url(r'^settings/', views.settings_page, name='settings_page'),
    url(r'^$', views.main_page, name='main_page'),
]