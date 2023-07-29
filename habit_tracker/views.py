from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from habit_tracker.models import PleasantHabit, GoodHabit
from habit_tracker.paginations import HabitPagination
from habit_tracker.permissions import IsOwner
from habit_tracker.serializers import PleasantHabitSerializer, GoodHabitSerializer, GoodHabitCreateSerializer
from habit_tracker.services import MailingHabitService
from habit_tracker.tasks import send_a_task


class PleasantHabitViewSet(viewsets.ModelViewSet):
    """Представление для приятных привычек, включающее в себя весь механизм CRUD"""
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Пользователь может видеть только свои приятные привычки с признаком приятной привычки"""
        user = self.request.user
        if user.is_staff:
            return PleasantHabit.objects.all()
        else:
            return PleasantHabit.objects.filter(user=user, is_pleasant_habit=True)

    def perform_create(self, serializer):
        """При создании приятной привычки присваивается автор"""
        serializer.save(user=self.request.user)


class PleasantPublishedHabitListAPIViewSet(generics.ListAPIView):
    """Представление для списка публичных приятных привычек"""
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class GoodHabitListAPIView(generics.ListAPIView):
    """Представление для просмотра полезных привычек"""
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Пользователь может видеть только свои полезные привычки"""
        user = self.request.user
        if user.is_staff:
            return GoodHabit.objects.all()
        else:
            return GoodHabit.objects.filter(user=user, is_published=True)


class GoodHabitIsPublishedListAPIView(generics.ListAPIView):
    """Представление для списка публичных полезных привычек"""
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class GoodHabitCreateAPIView(generics.CreateAPIView):
    """Представление для создания полезной привычки"""
    serializer_class = GoodHabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """При создании полезной привычки присваивается автор"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        habit = GoodHabit.objects.get(id=serializer.data['id'])
        if habit.is_published:
            # создание периодической задачи, которая отправляет автору напоминание о выполнении действия
            telegram_message = MailingHabitService(habit)
            telegram_message.create_task()
            # отправка автору сообщения с полезной привычкой
            send_a_task(habit.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GoodHabitRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра одной полезной привычки"""
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsAuthenticated]


class GoodHabitUpdateAPIView(generics.UpdateAPIView):
    """Представления для обновления полезной привычки"""
    serializer_class = GoodHabitCreateSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]


class GoodHabitDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления полезной привычки"""
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]
