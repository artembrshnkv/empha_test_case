from .models import ReservedRoom


def booked_room_date_is_correct(cleaned_data):
    room_book_dates = \
        ReservedRoom.objects.filter(number_id=cleaned_data['number']).\
        values('start_reservation', 'end_reservation')
    asked_data_available = False

    for book in room_book_dates:
        if not cleaned_data['start_reservation'] < book['start_reservation'] and \
                cleaned_data['end_reservation'] < book['start_reservation'] or \
                cleaned_data['start_reservation'] > book['end_reservation'] and \
                cleaned_data['end_reservation'] > book['end_reservation']:
            asked_data_available = True

    if not room_book_dates:
        asked_data_available = True

    date_range_is_correct = False
    if cleaned_data['end_reservation'] > cleaned_data['start_reservation']:
        date_range_is_correct = True

    return True if asked_data_available and date_range_is_correct else False
