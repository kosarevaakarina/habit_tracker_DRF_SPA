from rest_framework import serializers

from habit_tracker.models import PleasantHabit, GoodHabit


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор представления приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = ('place', 'time', 'action', 'duration', 'is_pleasant_habit')


class GoodHabitSerializer(serializers.ModelSerializer):
    """Сериализатор представления полезной привычки"""

    pleasant_habit = PleasantHabitSerializer()

    class Meta:
        model = GoodHabit
        fields = ('user', 'place', 'time', 'action', 'duration', 'frequency', 'pleasant_habit', 'reward')
