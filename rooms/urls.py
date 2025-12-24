from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/add/', views.RoomCreateView.as_view(), name='room_add'),
    path('room/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room_edit'),
    path('room/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),

    path('booking/add/<int:room_id>/', views.BookingCreateView.as_view(), name='booking_add'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('my/', views.MyBookingsView.as_view(), name='my_bookings'),

    path('export/excel/', views.export_rooms_excel, name='export_excel'),
    path('export/pdf/', views.export_bookings_pdf, name='export_pdf'),
]