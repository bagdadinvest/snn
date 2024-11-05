# your_app/templatetags/static_content.py
import os
from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def include_static_files(directory):
    static_dir = os.path.join(settings.STATIC_ROOT, directory)
    if not os.path.exists(static_dir):
        return ''
    files = [os.path.join(directory, f) for f in os.listdir(static_dir)]
    links = []
    for file in files:
        if file.endswith('.css'):
            links.append(f'<link rel="stylesheet" type="text/css" href="{static(file)}">')
        elif file.endswith('.js'):
            links.append(f'<script src="{static(file)}"></script>')
    return ''.join(links)
