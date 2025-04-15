from django.conf import settings
from django.db import models

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


type LanguageName = str
type LanguageAlias = str
type LanguageFilename = str
type LanguageMimeType = str
type StyleName = str

type LanguageLexer = tuple[
    LanguageName,
    tuple[LanguageAlias],
    tuple[LanguageFilename],
    tuple[LanguageMimeType],
]
type FormatterLanguage = tuple[LanguageAlias, LanguageName]
type FormatterStyle = tuple[StyleName, StyleName]


def load_lexers() -> list[LanguageLexer]:
    return [item for item in get_all_lexers() if item[1]]


def load_languages() -> list[FormatterLanguage]:
    items: list[FormatterLanguage] = [(item[1][0], item[0]) for item in LEXERS]
    return sorted(items)


def load_styles() -> list[FormatterStyle]:
    items: list[FormatterStyle] = [(item, item) for item in get_all_styles()]
    return sorted(items)


LEXERS = load_lexers()
LANGUAGE_CHOICES = load_languages()
STYLE_CHOICES = load_styles()

DEFAULT_TITLE = ""
DEFAULT_LANGUAGE = "python"
DEFAULT_STYLE = "friendly"


def get_formatter(linenos: bool | str, title: str, style: str) -> HtmlFormatter:
    linenos = "table" if linenos else False
    options: dict[str, str] = {"title": title} if title else {}

    return HtmlFormatter(style=style, linenos=linenos, full=True, **options)


class Snippet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="snippets", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    code = models.TextField()
    highlighted = models.TextField()

    title = models.CharField(max_length=100, blank=True, default=DEFAULT_TITLE)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default=DEFAULT_LANGUAGE, max_length=100
    )
    style = models.CharField(
        choices=STYLE_CHOICES, default=DEFAULT_STYLE, max_length=100
    )
    linenos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Use the `pygments` library to create a highlighted HTML representation of the code snippet."""
        lexer = get_lexer_by_name(self.language)
        formatter = get_formatter(self.linenos, self.title, self.style)

        self.highlighted = highlight(self.code, lexer, formatter)  # noqa: WPS601
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]
