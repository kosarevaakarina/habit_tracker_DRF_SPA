from django.contrib import admin

from habit_tracker.models import PleasantHabit, GoodHabit


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'duration', 'place')


@admin.register(GoodHabit)
class GoodHabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'duration', 'place')
