from django.urls import URLPattern, URLResolver, path

from polls import views


app_name: str = "polls"
urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
