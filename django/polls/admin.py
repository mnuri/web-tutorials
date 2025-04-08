import datetime

from django.contrib import admin
from django.utils import timezone

from polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Data", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self, obj: Question) -> bool:
        now: datetime.datetime = timezone.now()
        return now - datetime.timedelta(days=1) <= obj.pub_date <= now


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
