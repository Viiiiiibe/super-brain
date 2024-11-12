from django import template
from django.apps import apps

register = template.Library()


@register.filter
def is_instance(obj, model_name):
    model = apps.get_model('courses', model_name)
    return isinstance(obj, model)


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def with_placeholder(field, placeholder_text):
    field.field.widget.attrs.update({'placeholder': placeholder_text})
    return field
