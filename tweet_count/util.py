import json

from django.http import HttpResponse


def json_response(func):
    """
    Decorator to make responding with JSON easy.
    First thing returned must be JSON serializable,
    second thing is a dict of kwargs to be passed to
    Django's HttpResponse

    Also able to be used like a regular function

    Usage:

    @json_response
    def my_view(request):
        return {
            'something': 'hello'
        }

    @json_response
    def my_404_view(request):
        return {
            'error': 'resource not found'
        }, {'status': 404}

    def another_view(request):
        response = json_response({
            'data': True
        })

        response.set_cookie('test', '1')
        return respose
    """

    def respond(source_dict, *a, **kw):
        kw['content_type'] = 'application/json'
        return HttpResponse(
            json.dumps(source_dict, indent=4),
            *a,
            **kw
        )

    def inner(request, *a, **kw):
        output = func(request, *a, **kw)
        return json_response(output)

    if isinstance(func, (dict, list)):
        return respond(func)
    elif isinstance(func, tuple):
        return respond(func[0], **func[1])
    else:
        # being used as a decorator
        return inner
