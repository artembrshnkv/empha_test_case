from django.contrib import admin
from .models import Room, ReservedRoom


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'price', 'quantity']
    list_display_links = ['number']
    prepopulated_fields = {'slug': ('number', )}


@admin.register(ReservedRoom)
class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_id', 'user_id', 'time_reservation',
                    'start_reservation', 'end_reservation']
    list_display_links = ['number_id']
