from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Room(models.Model):
    number = models.IntegerField(verbose_name='Номер', unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    price = models.IntegerField(verbose_name='Цена')
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.number}'

    def get_absolute_url(self):
        return reverse('show_room', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class ReservedRoom(models.Model):
    number = models.ForeignKey(
        verbose_name='Номер',
        to=Room,
        on_delete=models.PROTECT)
    user = models.ForeignKey(
        verbose_name='Человек',
        to=User,
        on_delete=models.PROTECT)
    time_reservation = models.DateField(
        verbose_name='Дата брони', auto_now_add=True)
    start_reservation = models.DateField(verbose_name='Начало брони')
    end_reservation = models.DateField(verbose_name='Конец брони')

    def get_absolute_url(self):
        return reverse('delete_booking', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'Забронированная комната'
        verbose_name_plural = 'Забронированные комнаты'
