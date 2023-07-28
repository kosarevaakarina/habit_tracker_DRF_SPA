from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from habit_tracker.models import PleasantHabit, GoodHabit
from habit_tracker.paginations import HabitPagination
from habit_tracker.permissions import IsOwner
from habit_tracker.serializers import PleasantHabitSerializer, GoodHabitListSerializer, \
    GoodHabitSerializer


class PleasantHabitViewSet(viewsets.ModelViewSet):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PleasantHabit.objects.all()
        else:
            return PleasantHabit.objects.filter(user=user, is_pleasant_habit=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PleasantHabitIsPublishedListAPIViewSet(generics.ListAPIView):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class GoodHabitListAPIView(generics.ListAPIView):
    serializer_class = GoodHabitListSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return GoodHabit.objects.all()
        else:
            return GoodHabit.objects.filter(user=user, is_published=True)


class GoodHabitIsPublishedListAPIView(generics.ListAPIView):
    serializer_class = GoodHabitListSerializer
    queryset = GoodHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class GoodHabitCreateAPIView(generics.CreateAPIView):
    serializer_class = GoodHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoodHabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsAuthenticated]


class GoodHabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]


class GoodHabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]
