from rest_framework import serializers
from rest_framework.serializers import ValidationError

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

    def validate(self, attrs):
        if booked_room_date_is_correct(attrs):
            return attrs

        raise ValidationError('validation error')

    def save(self, **kwargs):
        ReservedRoom.objects.create(**self.validated_data)

    def destroy(self):
        ReservedRoom.objects.get(pk=self.validated_data['id']).delete()
