from django import template

register = template.Library()


@register.filter(name='cut')
def cut(string, arg):
    string = string.replace(arg, '')
    return string

