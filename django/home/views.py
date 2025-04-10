from django.http import HttpResponse


def index(request):
    return HttpResponse("I am root")


def hello(request, hello_name):
    return HttpResponse(f"Hello {hello_name}")
