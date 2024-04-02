from django import template

register = template.Library()

@register.filter
def reverse_range(value):
    return range(value, 0, -1)

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key, {})

@register.filter
def subtract(value, arg):
    return value - arg
