from django import template

from mainapp.utils import booked_room_date_is_correct

register = template.Library()


@register.simple_tag
def check_date(form):
    return True if not booked_room_date_is_correct(form.cleaned_data) else False
