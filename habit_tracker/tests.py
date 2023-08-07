from rest_framework.test import APITestCase
from rest_framework import status
from habit_tracker.models import PleasantHabit, GoodHabit
from users.models import User


class UserCreate(APITestCase):
    def setUp(self):
        """Создание экземпляров приятной и полезной привычки"""
        # экземпляр приятной привычки
        self.pleasant_habit = PleasantHabit.objects.create(place='TestPlace',
                                                           time='07:00',
                                                           action='TestAction',
                                                           duration=100,
                                                           )
        # экземпляр полезной привычки
        self.good_habit = GoodHabit.objects.create(place='HabitPlace',
                                                   time='19:00',
                                                   action='HabitAction',
                                                   duration=20,
                                                   reward='TestReward'
                                                   )

    def create_user(self):
        """Создание и авторизация пользователя"""
        self.email = 'example@test.ru'
        self.tg_username = 'telegramtest'
        self.user = User(email=self.email, tg_username=self.tg_username, is_staff=True)
        self.user.set_password('123Qaz')
        self.user.save()
        response = self.client.post(
            '/users/token/',
            {
                'email': self.email,
                'password': '123Qaz'
            }
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def pleasant_habit_for_auth_user(self):
        """Привязка авторизованного пользователя к приятной привычке"""
        self.create_user()
        self.pleasant_habit.user = self.user
        self.pleasant_habit.save()
        return self.pleasant_habit

    def good_habit_for_auth_user(self):
        """Привязка авторизованного пользователя к полезной привычке"""
        self.create_user()
        self.good_habit.user = self.user
        self.good_habit.save()
        return self.good_habit


class PleasantHabitTestCase(UserCreate):
    """Тестирование представления приятной привычки"""

    def test_post_pleasant_habit(self):
        """Тестирование создания приятной привычки"""
        self.pleasant_habit_for_auth_user()
        response = self.client.post('/pleasant-habit/', {'place': 'TestPlace',
                                                         'time': '07:00',
                                                         'action': 'NewTestAction',
                                                         'duration': 100})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_fail_1_pleasant_habit(self):
        """Тестирование создания приятной привычки (не выполняется условие уникальности для поля 'action')"""
        self.pleasant_habit_for_auth_user()
        response = self.client.post('/pleasant-habit/', {'action': 'TestAction',
                                                         'time': '20:00',
                                                         'place': 'TestPlace',
                                                         'duration': 50})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_fail_2_pleasant_habit(self):
        """Тестирование создания приятной привычки (не выполняется условие 'duration' < 120)"""
        self.pleasant_habit_for_auth_user()
        response = self.client.post('/pleasant-habit/', {'action': 'TestAction!',
                                                         'time': '20:00',
                                                         'place': 'TestPlace',
                                                         'duration': 150})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_pleasant_habit(self):
        """Тестирование просмотра приятных привычек"""
        self.pleasant_habit_for_auth_user()
        response = self.client.get('/pleasant-habit/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'place': 'TestPlace',
                  'time': '07:00:00',
                  'action': 'TestAction',
                  'duration': 100,
                  'is_pleasant_habit': True}]}
        )

    def test_get_pleasant_habit_is_published(self):
        """Тестирование просмотра приятных привычек"""
        self.pleasant_habit_for_auth_user()
        response = self.client.get('/pleasant-habit-is-published/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [{
                'place': 'TestPlace',
                'time': '07:00:00',
                'action': 'TestAction',
                'duration': 100,
                'is_pleasant_habit': True
            }]

        )

    def test_retrieve_pleasant_habit(self):
        """Тестирование просмотра одной приятной привычки"""
        pleasant_habit = self.pleasant_habit_for_auth_user()
        response = self.client.get(f'/pleasant-habit/{pleasant_habit.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'place': 'TestPlace',
             'time': '07:00:00',
             'action': 'TestAction',
             'duration': 100,
             'is_pleasant_habit': True}

        )

    def test_update_pleasant_habit(self):
        """Тестирование обновления приятной привычки"""
        pleasant_habit = self.pleasant_habit_for_auth_user()
        response = self.client.patch(f'/pleasant-habit/{pleasant_habit.id}/', {'action': 'UpdateAction',
                                                                               'duration': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'place': 'TestPlace',
             'time': '07:00:00',
             'action': 'UpdateAction',
             'duration': 20,
             'is_pleasant_habit': True}
        )

    def test_delete_pleasant_habit(self):
        """Тестирование удаления приятной привычки"""
        pleasant_habit = self.pleasant_habit_for_auth_user()
        response = self.client.delete(f'/pleasant-habit/{pleasant_habit.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GoodHabitTestCase(UserCreate):
    """Тестирование представления полезной привычки"""

    def test_post_good_habit(self):
        """Тестирование создания полезной привычки"""
        self.good_habit_for_auth_user()
        response = self.client.post('/good-habit/create/', {'place': 'TestPlace',
                                                            'time': '07:00',
                                                            'action': 'GoodHabitTest',
                                                            'duration': 100,
                                                            'reward': 'testReward'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_fail_1_good_habit(self):
        """Тестирование создания полезной привычки (не выполняется условие уникальности для поля 'action')"""
        self.good_habit_for_auth_user()
        response = self.client.post('/good-habit/create/', {'place': 'TestPlace',
                                                            'time': '07:00',
                                                            'action': 'HabitAction',
                                                            'duration': 100,
                                                            'reward': 'testReward'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_fail_2_good_habit(self):
        """Тестирование создания полезной привычки (не выполняется условие 'duration' < 120)"""
        self.good_habit_for_auth_user()
        response = self.client.post('/good-habit/create/', {'place': 'TestPlace',
                                                            'time': '07:00',
                                                            'action': 'GoodAction',
                                                            'duration': 180,
                                                            'reward': 'testReward'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_fail_3_good_habit(self):
        """Тестирование создания полезной привычки
        (не выполняется условие: невозможен одновременный выбор приятной привычки и приятного действия)"""
        self.good_habit_for_auth_user()
        response = self.client.post('/good-habit/create/', {'place': 'TestPlace',
                                                            'time': '07:00',
                                                            'action': 'GoodAction',
                                                            'duration': 180,
                                                            'reward': 'testReward',
                                                            'pleasant_habit': self.pleasant_habit.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_good_habit(self):
        """Тестирование просмотра полезных привычек"""
        self.good_habit_for_auth_user()
        response = self.client.get('/good-habit/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{'user': self.user.pk,
                          'place': 'HabitPlace',
                          'time': '19:00:00',
                          'action': 'HabitAction',
                          'duration': 20,
                          'frequency': 'EVERY DAY',
                          'pleasant_habit': None,
                          'reward': 'TestReward'}]}

        )

    def test_get_good_habit_is_published(self):
        """Тестирование просмотра полезных привычек"""
        self.good_habit_for_auth_user()
        response = self.client.get('/good-habit-is-published/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [{
                'user': self.user.pk,
                'place': 'HabitPlace',
                'time': '19:00:00',
                'action': 'HabitAction',
                'duration': 20,
                'frequency': 'EVERY DAY',
                'pleasant_habit': None,
                'reward': 'TestReward'
            }]

        )

    def test_retrieve_good_habit(self):
        """Тестирование просмотра одной полезной привычки"""
        good_habit = self.good_habit_for_auth_user()
        response = self.client.get(f'/good-habit/{good_habit.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'user': self.user.pk,
             'place': 'HabitPlace',
             'time': '19:00:00',
             'action': 'HabitAction',
             'duration': 20,
             'frequency': 'EVERY DAY',
             'pleasant_habit': None,
             'reward': 'TestReward'}
        )

    def test_update_good_habit(self):
        """Тестирование обновления полезной привычки"""
        good_habit = self.good_habit_for_auth_user()
        response = self.client.patch(f'/good-habit/update/{good_habit.id}/', {'action': 'UpdateAction',
                                                                              'duration': 90,
                                                                              'place': 'NewTestPlace',
                                                                              'time': '19:00',
                                                                              'reward': 'NewTestReward'
                                                                              })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'id': good_habit.pk,
             'user': self.user.pk,
             'place': 'NewTestPlace',
             'time': '19:00:00',
             'action': 'UpdateAction',
             'duration': 90,
             'frequency': 'EVERY DAY',
             'pleasant_habit': None,
             'reward': 'NewTestReward'}

        )

    def test_delete_good_habit(self):
        """Тестирование удаления полезной привычки"""
        good_habit = self.good_habit_for_auth_user()
        response = self.client.delete(f'/good-habit/delete/{good_habit.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
