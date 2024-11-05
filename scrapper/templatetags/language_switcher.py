from django import template
from django.urls import resolve, reverse
from wagtail.models import Locale

register = template.Library()

@register.simple_tag(takes_context=True)
def language_switcher(context, lang_code):
    request = context['request']
    current_path = request.path

    # Split the path to check for a language code prefix
    path_parts = current_path.strip('/').split('/')
    if path_parts[0] in ['en', 'tr']:  # Adjust to your supported language codes
        # Replace the first part (current language code) with the new language code
        path_parts[0] = lang_code
    else:
        # If there's no language code prefix, add the new one
        path_parts.insert(0, lang_code)

    # Reconstruct the path with the new language code prefix
    new_path = '/' + '/'.join(path_parts)
    return new_path
