from django.urls import path
from rest_framework.routers import DefaultRouter

from habit_tracker.views import *

router = DefaultRouter()
router.register(r'pleasant-habit', PleasantHabitViewSet, basename='pleasant_habit')

urlpatterns = [
    path('pleasant-habit-is-published/', PleasantHabitIsPublishedListAPIViewSet.as_view(),
         name='pleasant_habit_is_published'),
    path('good-habit/', GoodHabitListAPIView.as_view(), name='good_habit_list'),
    path('good-habit-is-published/', GoodHabitIsPublishedListAPIView.as_view(), name='good_habit_is_published'),
    path('good-habit/<int:pk>/', GoodHabitRetrieveAPIView.as_view(), name='good_habit_detail'),
    path('good-habit/create/', GoodHabitCreateAPIView.as_view(), name='good_habit_create'),
    path('good-habit/update/', GoodHabitUpdateAPIView.as_view(), name='good_habit_update'),
    path('good-habit/delete/', GoodHabitDestroyAPIView.as_view(), name='good_habit_delete')
              ] + router.urls
