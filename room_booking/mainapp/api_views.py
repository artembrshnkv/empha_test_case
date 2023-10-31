from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomSerializer, ReservedRoomSerializer
from .models import Room, ReservedRoom


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserBookedRooms(ReadOnlyModelViewSet):
    serializer_class = ReservedRoomSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return ReservedRoom.objects.filter(user_id=self.request.user.pk)
