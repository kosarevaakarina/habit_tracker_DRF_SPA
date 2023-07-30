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
    date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, unique=True, verbose_name='действие')
    duration = models.PositiveIntegerField(default=120, verbose_name='длительность выполнений в секундах')
    is_published = models.BooleanField(default=True, verbose_name='признак публичности привычки')


class PleasantHabit(Habit):
    """Модель приятной привычки"""
    is_pleasant_habit = models.BooleanField(default=True, verbose_name='признак приятной привычки')

    class Meta:
        verbose_name = 'приятная привычка'
        verbose_name_plural = 'приятные привычки'

    def __str__(self):
        return f'{self.action}, время: {self.time}, место: {self.place}, выполнить за {self.duration} секунд'

    def delete(self, using=None, keep_parents=False):
        self.is_pleasant_habit = False
        self.is_published = False
        self.save()


class GoodHabit(Habit):
    """Модель полезной привычки"""
    pleasant_habit = models.ForeignKey(PleasantHabit, on_delete=models.CASCADE, verbose_name='приятная привычка',
                                       **NULLABLE)
    reward = models.TextField(verbose_name='вознаграждение', **NULLABLE)
    frequency = models.CharField(max_length=100, default='EVERY DAY', choices=FREQUENCY, verbose_name='Периодичность')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'
        ordering = ('time',)

    def __str__(self):
        return f'Задание: {self.action}, время: {self.time}, место: {self.place}, выполнить за {self.duration} ' \
               f'секунд (приятное действие: {self.pleasant_habit if self.pleasant_habit else self.reward})'

    def delete(self, using=None, keep_parents=False):
        self.is_published = False
        self.save()
