from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from pastebin.models import Snippet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippet-detail", read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "snippets"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight",
        format="html",
    )

    class Meta:
        model = Snippet
        fields = [
            "id",
            "owner",
            "code",
            "highlight",
            "title",
            "url",
            "linenos",
            "language",
            "style",
        ]
