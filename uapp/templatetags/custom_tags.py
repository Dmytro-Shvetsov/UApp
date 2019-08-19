from django import template

register = template.Library()


@register.filter(name='cut')
def cut(string, arg):
    string = string.replace(arg, '')
    return string


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
