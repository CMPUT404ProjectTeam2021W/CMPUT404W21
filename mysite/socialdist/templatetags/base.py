from django import template
#code from https://www.programmersought.com/article/8685697628/ 
# code by ????? 
from markdown import markdown 
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe = True)
def custom_markdown(value):
    return mark_safe(markdown(value,
                              extensions = ['markdown.extensions.extra',
                                            'markdown.extensions.toc',
                                            'markdown.extensions.sane_lists',
                                            'markdown.extensions.nl2br',
                                            'markdown.extensions.codehilite',],
                              safe_mode = True,
                              enable_attributes = False))