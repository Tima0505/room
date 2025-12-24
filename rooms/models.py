from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class Room(models.Model):
    name = models.CharField("Название комнаты", max_length=100)
    capacity = models.PositiveIntegerField("Вместимость")
    location = models.CharField("Расположение", max_length=200, blank=True)
    equipments = models.ManyToManyField(Equipment, verbose_name="Оборудование", blank=True)
    image = models.ImageField("Фото", upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.capacity} чел.)"

    class Meta:
        verbose_name = "Переговорная"
        verbose_name_plural = "Переговорные"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Ожидает'),
        ('A', 'Подтверждено'),
        ('R', 'Отменено'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    title = models.CharField("Тема встречи", max_length=200)
    start = models.DateTimeField("Начало")
    end = models.DateTimeField("Конец")
    attendees = models.PositiveIntegerField("Участников", default=1)
    equipment = models.ManyToManyField(Equipment, verbose_name="Доп. оборудование", blank=True)
    status = models.CharField("Статус", max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.room} | {self.start.date()}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ['-start']