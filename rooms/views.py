from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import openpyxl
from .models import Room, Booking
from .forms import RoomForm, BookingForm

# === Комнаты ===
class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room_list')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room_list')

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:room_list')

# === Бронирование ===
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'rooms/booking_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['room_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.room  # ← ЭТА СТРОКА РЕШАЕТ ПРОБЛЕМУ!
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.room = self.room
        booking.user = self.request.user

        # Проверка пересечения
        conflict = Booking.objects.filter(
            room=self.room,
            start__lt=booking.end,
            end__gt=booking.start,
            status__in=['P', 'A']
        ).exists()

        if conflict:
            form.add_error(None, 'Этот временной слот уже занят!')
            return self.form_invalid(form)

        booking.save()
        form.save_m2m()

        # Отправка email
        from .utils import send_booking_email
        send_booking_email(booking)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rooms:booking_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['room_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.room = self.room
        booking.user = self.request.user

        # Проверка пересечения
        conflict = Booking.objects.filter(
            room=self.room,
            start__lt=booking.end,
            end__gt=booking.start,
            status__in=['P', 'A']
        ).exists()

        if conflict:
            form.add_error(None, 'Этот временной слот уже занят!')
            return self.form_invalid(form)

        booking.save()
        form.save_m2m()

        # Отправка email
        from .utils import send_booking_email
        send_booking_email(booking)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rooms:booking_detail', kwargs={'pk': self.object.pk})

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'rooms/booking_detail.html'

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'rooms/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# === Экспорт ===
def export_rooms_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Загрузка переговорных"
    ws.append(['ID', 'Название', 'Вместимость', 'Локация', 'Оборудование'])
    for room in Room.objects.all():
        eq = ', '.join([e.name for e in room.equipments.all()])
        ws.append([room.id, room.name, room.capacity, room.location or '-', eq])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rooms.xlsx'
    wb.save(response)
    return response

def export_bookings_pdf(request):
    bookings = Booking.objects.all().order_by('start')
    html = render_to_string('rooms/bookings_pdf.html', {'bookings': bookings})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=bookings.pdf'
    pisa.CreatePDF(html, dest=response)
    return response