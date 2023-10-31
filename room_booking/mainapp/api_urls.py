from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .api_views import RoomViewSet, UserBookedRooms

room_router = SimpleRouter()
room_router.register('rooms', RoomViewSet)

booked_rooms_router = SimpleRouter()
booked_rooms_router.register('user_booked_rooms',
                             UserBookedRooms,
                             basename='reservedroom')

urlpatterns = [
    path('', include(room_router.urls)),
    path('', include(booked_rooms_router.urls)),
    path('', include('rest_framework.urls')),
]
