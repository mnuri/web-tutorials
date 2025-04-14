from django.urls import include, path

from rest_framework.routers import DefaultRouter

from pastebin import views


router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"groups", views.GroupViewSet, basename="group")
router.register(r"snippets", views.SnippetViewSet, basename="snippet")


urlpatterns = [
    path("", views.api_root),
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
