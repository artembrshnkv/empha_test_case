from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RoomSerializer, ReservedRoomSerializer
from .models import Room, ReservedRoom
from .filters import RoomFilter, RoomAndReservedRoomFilterBackend


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # filter_backends = [RoomAndReservedRoomFilterBackend]
    filterset_class = RoomFilter


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
