from django.urls import path
from rest_framework.routers import DefaultRouter

from habit_tracker.views import *

router = DefaultRouter()
router.register(r'pleasant_habit', PleasantHabitViewSet, basename='pleasant_habit')

urlpatterns = [
    path('good-habit/', GoodHabitListAPIView.as_view(), name='good_habit_list'),
    path('good-habit/<int:pk>/', GoodHabitRetrieveAPIView.as_view(), name='good_habit_detail'),
    path('good-habit/create/', GoodHabitCreateAPIView.as_view(), name='good_habit_create'),
    path('good-habit/update/', GoodHabitUpdateAPIView.as_view(), name='good_habit_update'),
    path('good-habit/delete/', GoodHabitDestroyAPIView.as_view(), name='good_habit_delete')
              ] + router.urls
