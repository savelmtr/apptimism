from django.template import Library

register = Library()


@register.simple_tag
def get_translated_car_name(obj, lang):
    return getattr(obj, f'name_{lang}')
