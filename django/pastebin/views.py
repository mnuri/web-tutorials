from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from pastebin.models import Snippet
from pastebin.permissions import IsOwnerOrReadOnly
from pastebin.renderers import PlainTextRenderer
from pastebin.serializers import GroupSerializer, SnippetSerializer, UserSerializer


@api_view(["GET"])
def api_root(request, format=None) -> Response:
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "groups": reverse("group-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(
        detail=True,
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.StaticHTMLRenderer,
            PlainTextRenderer,
        ],
    )
    def highlight(self, request, *args, **kwargs) -> Response:
        snippet: Snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
