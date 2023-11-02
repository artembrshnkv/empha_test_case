from rest_framework import serializers

from .models import Room, ReservedRoom
from .utils import booked_room_date_is_correct


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['number', 'price', 'quantity']
        model = Room


class ReservedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'time_reservation', 'start_reservation',
                  'end_reservation', 'number', 'user']
        model = ReservedRoom

    def save(self, **kwargs):
        if booked_room_date_is_correct(self.validated_data):
            ReservedRoom.objects.create(**self.validated_data)

    def destroy(self):
        ReservedRoom.objects.get(pk=self.validated_data['id']).delete()
