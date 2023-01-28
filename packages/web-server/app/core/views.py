import os

from django.conf import settings
from django.views.generic.base import TemplateView


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO - get Images and attach to context for rendering in template
        files = os.listdir(os.path.join(settings.STATIC_URL, '2021-09-05'))

        context['files'] = files

        return context
