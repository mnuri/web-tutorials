from django.contrib import admin

from pastebin.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ("highlighted", "updated_at", "created_at", "owner")


admin.site.register(Snippet, SnippetAdmin)
