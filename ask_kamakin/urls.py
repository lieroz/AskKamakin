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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ask import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/', views.sign_in_page, name='sign_in_page'),
    url(r'^sign_up/', views.sign_up_page, name='sign_up_page'),
    url(r'^ask/', views.ask_page, name='ask_page'),
    url(r'^answer/', views.answer_page, name='answer_page'),
    url(r'^settings/', views.settings_page, name='settings_page'),
    url(r'^$', views.main_page, name='main_page'),
]


