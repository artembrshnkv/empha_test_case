from rest_framework import serializers

from .models import Room, ReservedRoom


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Room


class ReservedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ReservedRoom

