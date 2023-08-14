from django import template

register = template.Library()

@register.filter
def split_description(value):
    lines = value.split('\n')
    return [(lines[i], lines[i + 1]) for i in range(0, len(lines), 2)]
