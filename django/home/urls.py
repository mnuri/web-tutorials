from django.urls import path

from home import views


urlpatterns = [
    path("", views.index, name="root_path"),
    path("hello/<hello_name>", views.hello, name="hello_path"),
]
