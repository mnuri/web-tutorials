from django.urls import URLPattern, URLResolver, path

from home import views


app_name: str = "home"
urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.IndexView.as_view(), name="home"),
    path("hello/", views.HelloView.as_view(), name="hello"),
    path("hello/<str:hello_name>/", views.SayHelloView.as_view(), name="say_hello"),
]
