from django.contrib import admin
from .models import Room, Equipment, Booking

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location')
    list_filter = ('capacity',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'user', 'start', 'end', 'status')
    list_filter = ('status', 'room', 'start')
    search_fields = ('title', 'user__username')