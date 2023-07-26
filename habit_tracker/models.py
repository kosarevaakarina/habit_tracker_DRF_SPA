from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}
FREQUENCY = [
    ('EVERY DAY', 'раз в день'),
    ('EVERY OTHER DAY', 'через день'),
    ('EVERY WEEK', 'раз в неделю'),
]


class Habit(models.Model):
    """Модель привычки"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='создатель привычки',
                             **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, unique=True, verbose_name='действие')
    duration = models.IntegerField(default=120, verbose_name='длительность выполнений в секундах')
    is_published = models.BooleanField(default=True, verbose_name='признак публичности привычки')


class PleasantHabit(Habit):
    """Модель приятной привычки"""
    is_pleasant_habit = models.BooleanField(default=True, verbose_name='признак приятной привычки')

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'

    def __str__(self):
        return f'Приятная привычка {self.action}, место: {self.place}, время: {self.time}'


class GoodHabit(Habit):
    """Модель полезной привычки"""
    pleasant_habit = models.ForeignKey(PleasantHabit, on_delete=models.CASCADE, verbose_name='приятная привычка', **NULLABLE)
    reward = models.TextField(verbose_name='вознаграждение', **NULLABLE)
    frequency = models.CharField(max_length=100, default='EVERY DAY', choices=FREQUENCY, verbose_name='Периодичность')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'

    def __str__(self):
        return f'Полезная привычка {self.action}, место: {self.place}, время: {self.time}'
