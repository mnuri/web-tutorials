from django.contrib import admin

from pastebin.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ("highlighted", "updated", "created", "owner")


admin.site.register(Snippet, SnippetAdmin)
