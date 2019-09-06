from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter(name='cut', is_safe=True)
def cut(string, arg):
    string = string.replace(arg, '')
    return string


@register.filter(name='get_item', is_safe=True)
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='add_value', is_safe=True)
@stringfilter
def add_value(input_tag, value):
    if value is not None:
        index = input_tag.find('>')
        input_tag = f"{input_tag[:index]} value='{value}' {input_tag[index:]}"
    return input_tag


@register.filter(name='get_like_dislike_color')
def get_like_dislike_color(value, estimType):
    if value == -1 and estimType == 'dislike':
        return 'text-danger'
    if value == 1 and estimType == 'like':
        return 'text-primary'
    return 'text-gray'

