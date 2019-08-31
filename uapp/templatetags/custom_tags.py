from django import template

register = template.Library()


@register.filter(name='cut')
def cut(string, arg):
    string = string.replace(arg, '')
    return string


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='styled_fa_icon')
def get_item(fa_icon, style):
    index = a.find('>')
    fa_icon = fa_icon[:index] + ' ' + style + fa_icon[index, :]
    return fa_icon
