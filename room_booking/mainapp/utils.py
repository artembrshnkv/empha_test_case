from .models import Room, ReservedRoom


def get_available_room_numbers(reservation_time):
    all_booked_rooms_dates = ReservedRoom.objects.all().\
        values('number', 'start_reservation', 'end_reservation')

    date_range_is_correct = False
    if reservation_time['end_reservation'] > reservation_time['start_reservation']:
        date_range_is_correct = True

    booked_rooms_numbers = []
    for booked_room in all_booked_rooms_dates:
        if booked_room['start_reservation'] <= reservation_time['start_reservation'] <=\
                booked_room['end_reservation'] or \
                booked_room['start_reservation'] <= reservation_time['end_reservation'] <=\
                booked_room['end_reservation']:
            booked_rooms_numbers.append(booked_room['number'])

    all_rooms_numbers = Room.objects.all().values('number')

    available_rooms_numbers = []
    for room in all_rooms_numbers:
        if room['number'] not in booked_rooms_numbers:
            available_rooms_numbers.append(room['number'])

    if date_range_is_correct:
        return available_rooms_numbers


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
