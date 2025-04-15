from django.utils.encoding import smart_str

from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = "text/plain"
    format = "txt"

    def render(self, data: str, accepted_media_type=None, renderer_context=None) -> str:
        return smart_str(data, encoding=self.charset)
