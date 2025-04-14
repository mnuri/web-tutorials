from django.conf import settings
from django.db import models

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


def load_lexers():
    return [item for item in get_all_lexers() if item[1]]


def load_lenguages():
    items = [(item[1][0], item[0]) for item in LEXERS]
    return sorted(items)


def load_styles():
    items = [(item, item) for item in get_all_styles()]
    return sorted(items)


LEXERS = load_lexers()
LANGUAGE_CHOICES = load_lenguages()
STYLE_CHOICES = load_styles()


def get_formatter(linenos: bool | str, title: str, style: str) -> HtmlFormatter:
    linenos = "table" if linenos else False
    options: dict[str, str] = {"title": title} if title else {}

    return HtmlFormatter(style=style, linenos=linenos, full=True, **options)


class Snippet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="snippets", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    code = models.TextField()
    highlighted = models.TextField()

    title = models.CharField(max_length=100, blank=True, default="")
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    linenos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Use the `pygments` library to create a highlighted HTML representation of the code snippet."""
        lexer = get_lexer_by_name(self.language)
        formatter = get_formatter(self.linenos, self.title, self.style)

        self.highlighted = highlight(self.code, lexer, formatter)  # noqa: WPS601
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created"]
