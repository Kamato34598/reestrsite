from django import template

register = template.Library()

@register.filter
def is_combined_form(form):
    return hasattr(form, 'is_combined_form') and form.is_combined_form