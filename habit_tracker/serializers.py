from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from habit_tracker.models import PleasantHabit, GoodHabit
from users.models import User
from users.serializers import UserSerializer


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор представления приятной привычки"""

    class Meta:
        model = PleasantHabit
        fields = ('place', 'time', 'action', 'duration', 'is_pleasant_habit')


class GoodHabitSerializer(serializers.ModelSerializer):
    """Сериализатор представления полезной привычки"""

    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())
    pleasant_habit = PleasantHabitSerializer()

    class Meta:
        model = GoodHabit
        fields = ('user', 'place', 'time', 'action', 'duration', 'frequency', 'pleasant_habit', 'reward')
