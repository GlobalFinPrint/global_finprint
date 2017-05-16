from django import template

register = template.Library()


@register.simple_tag()
def active_if_equal(value_1, value_2):
    return "active" if value_1 == value_2 else "notActive"
