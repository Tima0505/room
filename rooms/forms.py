from django import forms
from .models import Room, Booking

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'location', 'equipments', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['title', 'start', 'end', 'attendees', 'equipment']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end':   forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }