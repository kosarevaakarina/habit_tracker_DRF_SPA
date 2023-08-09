from django.urls import path
from rest_framework.routers import DefaultRouter

from habit_tracker.views import PleasantHabitViewSet, PleasantPublishedHabitListAPIViewSet, GoodHabitListAPIView, \
    GoodHabitIsPublishedListAPIView, GoodHabitRetrieveAPIView, GoodHabitCreateAPIView, GoodHabitUpdateAPIView, \
    GoodHabitDestroyAPIView

router = DefaultRouter()
router.register(r'pleasant-habit', PleasantHabitViewSet, basename='pleasant_habit')

urlpatterns = [
                  path('pleasant-habit-is-published/', PleasantPublishedHabitListAPIViewSet.as_view(),
                       name='pleasant_habit_is_published'),
                  path('good-habit/', GoodHabitListAPIView.as_view(), name='good_habit_list'),
                  path('good-habit-is-published/', GoodHabitIsPublishedListAPIView.as_view(),
                       name='good_habit_is_published'),
                  path('good-habit/<int:pk>/', GoodHabitRetrieveAPIView.as_view(), name='good_habit_detail'),
                  path('good-habit/create/', GoodHabitCreateAPIView.as_view(), name='good_habit_create'),
                  path('good-habit/update/<int:pk>/', GoodHabitUpdateAPIView.as_view(), name='good_habit_update'),
                  path('good-habit/delete/<int:pk>/', GoodHabitDestroyAPIView.as_view(), name='good_habit_delete')
              ] + router.urls
