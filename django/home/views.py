from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic


class IndexView(generic.TemplateView):
    template_name: str = "index.html"
    http_method_names: list[str] = ["get"]


class HelloView(generic.TemplateView):
    template_name: str = "hello.html"
    http_method_names: list[str] = ["get", "post"]

    def post(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
        hello_name: str = request.POST["hello_name"]

        if not hello_name:
            return render(
                request,
                "hello.html",
                {"error_message": "You didn't enter a name."},
                status=422,
            )

        return HttpResponseRedirect(reverse("home:say_hello", args=(hello_name,)))


class SayHelloView(generic.TemplateView):
    template_name = "say_hello.html"
    http_method_names = ["get"]

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        hello_name: str = kwargs["hello_name"]
        return render(request, "say_hello.html", {"hello_name": hello_name})
