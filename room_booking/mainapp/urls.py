from django.urls import path

from .views import *


urlpatterns = [
    path('', RoomList.as_view(), name='main_page'),
    path('reg', UserRegistration.as_view(), name='registration'),
    path('account', UserAccount.as_view(), name='account'),
    path('user_login', UserLogin.as_view(), name='user_login'),
    path('user_logout', user_logout, name='user_logout'),
    path('show_room/<slug:slug>', ShowRoom.as_view(), name='show_room'),
    path('book_room/<int:room_number>', BookRoom.as_view(), name='book_room'),
    path(
        'delete_booking/<int:pk>',
        DeleteBooking.as_view(),
        name='delete_booking'),
    # path('choose_date', SortByAvailableDates.as_view(), name='choose_date'),
]
