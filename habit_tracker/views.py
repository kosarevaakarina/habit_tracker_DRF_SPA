from rest_framework import viewsets, generics

from habit_tracker.models import PleasantHabit, GoodHabit
from habit_tracker.serializers import PleasantHabitSerializer, GoodHabitSerializer


class PleasantHabitViewSet(viewsets.ModelViewSet):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PleasantHabit.objects.all()
        else:
            return PleasantHabit.objects.filter(user=user, is_pleasant_habit=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoodHabitListAPIView(generics.ListAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return GoodHabit.objects.all()
        else:
            return GoodHabit.objects.filter(user=user)


class GoodHabitCreateAPIView(generics.CreateAPIView):
    serializer_class = GoodHabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoodHabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()


class GoodHabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()


class GoodHabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()

