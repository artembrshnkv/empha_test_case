from .models import ReservedRoom

menu = [
    {'title': 'Все номера', 'url': 'main_page', 'type': 'link_button'},
    {'title': 'Регистрация', 'url': 'registration', 'type': 'auth_false'},
    {'title': 'Вход', 'url': 'user_login', 'type': 'auth_false'},
    {'title': 'Аккаунт', 'url': 'account', 'type': 'auth_true'},
]

sort_menu = [
    {'title': 'По возрастанию цены', 'url': '?min_price=True'},
    {'title': 'По убыванию цены', 'url': '?max_price=True'},
    {'title': 'по возрастанию вместимости', 'url': '?min_quantity=True'},
    {'title': 'По убыванию вместимоси', 'url': '?max_quantity=True'}
]


class BaseMixin:
    def get_general_data(self, **kwargs):
        context = kwargs
        context['menu'] = menu

        return context


class BaseListMixin(BaseMixin):
    def get_general_data(self, **kwargs):
        context = super().get_general_data(**kwargs)
        context['sort_menu'] = sort_menu

        return context


def booked_room_date_is_correct(cleaned_data):
    room_book_dates = \
        ReservedRoom.objects.filter(number_id=cleaned_data['number']).values('start_reservation', 'end_reservation')
    asked_data_available = False

    for book in room_book_dates:
        if not cleaned_data['start_reservation'] < book['start_reservation'] and \
                cleaned_data['end_reservation'] < book['start_reservation'] or \
                cleaned_data['start_reservation'] > book['end_reservation'] and \
                cleaned_data['end_reservation'] > book['end_reservation']:
            asked_data_available = True

    date_range_is_correct = False
    if cleaned_data['end_reservation'] > cleaned_data['start_reservation']:
        date_range_is_correct = True

    return True if asked_data_available and date_range_is_correct else False

