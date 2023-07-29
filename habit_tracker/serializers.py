from rest_framework import serializers

from habit_tracker.models import PleasantHabit, GoodHabit
from habit_tracker.validators import HabitDurationValidator


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор представления приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = ('place', 'time', 'action', 'duration', 'is_pleasant_habit')
        validators = [HabitDurationValidator(field='duration')]


class GoodHabitCreateSerializer(serializers.ModelSerializer):
    """Сериализатор представления создания полезной привычки"""

    class Meta:
        model = GoodHabit
        fields = ('id', 'user', 'place', 'time', 'action', 'duration', 'frequency', 'pleasant_habit', 'reward')
        validators = [HabitDurationValidator(field='duration')]

    def validate(self, attrs):
        """Валидация данных"""
        if 'pleasant_habit' in attrs:
            pleasant_habit_id = attrs.get('pleasant_habit').id
            pleasant_habit = PleasantHabit.objects.filter(id=pleasant_habit_id).first()
            # Проверка признака приятной привычки
            if pleasant_habit.is_pleasant_habit is not True:
                raise serializers.ValidationError('Related habits can only include habits with a sign of a pleasant habit')
        # Проверка того, чтобы была выбрана или привычка, или действие
        if attrs.get('pleasant_habit') is None and attrs.get('reward') is None:
            raise serializers.ValidationError("You must choose a related habit or specify a reward!")
        # Исключение одновременного выбора связанной привычки и указания вознаграждения
        if attrs.get('pleasant_habit') and attrs.get('reward'):
            raise serializers.ValidationError(
                "It is not allowed to select a related habit and specify a reward at the same time!")
        return attrs


class GoodHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для представления полезных привычек"""
    pleasant_habit = PleasantHabitSerializer()

    class Meta:
        model = GoodHabit
        fields = ('user', 'place', 'time', 'action', 'duration', 'frequency', 'pleasant_habit', 'reward')
