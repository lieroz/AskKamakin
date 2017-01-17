from django.http import HttpResponse
import json


# Response ajax
class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
            content=json.dumps(kwargs),
            content_type='application/json',
        )


# Response ajax with error
class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
            status='error',
            code=code,
            message=message,
        )


def login_required_ajax(func):
    def check(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)

        return HttpResponseAjaxError(
            code='no_auth',
            message='Need auth'
        )

    return check
