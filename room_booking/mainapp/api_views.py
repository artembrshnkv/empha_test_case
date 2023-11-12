from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from .serializers import RoomSerializer, ReservedRoomSerializer
from .models import Room, ReservedRoom
from .filters import RoomFilter
from .utils import get_available_room_numbers

from datetime import date


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter

    def get_queryset(self):
        start_reservation = self.request.GET.get('start_reservation')
        end_reservation = self.request.GET.get('end_reservation')

        if start_reservation and end_reservation:
            start = start_reservation.split('-')
            end = end_reservation.split('-')

            reservation_time = {
                'start_reservation': date(int(start[0]),
                                          int(start[1]),
                                          int(start[2])),
                'end_reservation': date(int(end[0]),
                                        int(end[1]),
                                        int(end[2]))
            }
            available_room_numbers = get_available_room_numbers(reservation_time)

            return Room.objects.filter(number__in=available_room_numbers)


class UserBookedRooms(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    serializer_class = ReservedRoomSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return ReservedRoom.objects.filter(user_id=self.request.user.pk)

    def post(self):
        serializer = ReservedRoomSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
