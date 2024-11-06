from django import template
from django.apps import apps

register = template.Library()


@register.filter
def is_instance(obj, model_name):
    model = apps.get_model('courses', model_name)
    return isinstance(obj, model)
