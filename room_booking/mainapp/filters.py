from django_filters import rest_framework as filters

from .models import Room, ReservedRoom
from .utils import get_available_room_numbers


class RoomAndReservedRoomFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        filterset_class = super().get_filterset_class(view, queryset=None)

        return filterset_class


class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='lte')
    start_reservation = filters.DateFilter(method='date_is_available')
    end_reservation = filters.DateFilter(method='date_is_available')

    def date_is_available(self, queryset, name, value):
        if self.start_reservation and self.end_reservation:
            reservation_time = {
                'start_reservation': self.start_reservation,
                'end_reservation': self.end_reservation
            }

            available_room_numbers = get_available_room_numbers(reservation_time=reservation_time)
            return Room.objects.filter(number__in=available_room_numbers)


    class Meta:
        model = Room
        fields = ['price', 'quantity']
