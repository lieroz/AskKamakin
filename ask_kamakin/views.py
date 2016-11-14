import django.views.generic


class BasePage(django.views.generic.TemplateView):
    template_name = 'base.html'
