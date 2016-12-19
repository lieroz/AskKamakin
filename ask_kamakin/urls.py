"""ask_kamakin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from ask import views as ask_views

urlpatterns = [
    url(r'^login/?', ask_views.login, name='login'),
    url(r'^sign_up/?', ask_views.sign_up, name='sign_up'),
    url(r'^upload/?', ask_views.upload_file, name='upload'),
    # url(r'^question(?P<question_id>\d+)/', ask_views.question, name='question'),
    # url(r'^questions(?P<page>\d+)/', ask_views.question_page),
    url(r'^ask/?', ask_views.ask_page, name='ask_page'),
    url(r'^answer/?', ask_views.answer_page, name='answer_page'),
    url(r'^settings/?', ask_views.settings_page, name='settings_page'),
    url(r'^logout/?', ask_views.logout, name='logout'),
    url(r'^$', ask_views.main_page, name='main_page'),
    url(r'^admin/', admin.site.urls),
]


