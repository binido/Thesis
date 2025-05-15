from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def timesince_one_level(value):
    return timesince(value).split(",")[0]
