from django import template

from shop.models import ShoppingCart

register = template.Library()


@register.filter()
def min(value, arg):
    return value - arg
