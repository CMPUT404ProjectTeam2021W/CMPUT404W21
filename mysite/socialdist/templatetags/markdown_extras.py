from django import template
import markdown as md

from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions = ['markdown.extensions.fenced_code'])
