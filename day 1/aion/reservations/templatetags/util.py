from django import template
import datetime

register = template.Library()

@register.simple_tag
def date_or_string(value):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    else:
        return value
