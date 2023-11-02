from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins


from .serializers import RoomSerializer, ReservedRoomSerializer
from .models import Room, ReservedRoom


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        all_rooms = Room.objects.all()
        if self.request.GET.get('min_price'):
            queryset = all_rooms.order_by('price')
        elif self.request.GET.get('max_price'):
            queryset = all_rooms.order_by('-price')
        elif self.request.GET.get('min_quantity'):
            queryset = all_rooms.order_by('quantity')
        elif self.request.GET.get('max_quantity'):
            queryset = all_rooms.order_by('-quantity')
        else:
            queryset = all_rooms

        return queryset


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
