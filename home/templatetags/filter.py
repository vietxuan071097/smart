from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def format_num(num):
    return "{:,}".format(num) + " VNĐ"
