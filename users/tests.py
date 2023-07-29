from rest_framework import status

from habit_tracker.tests import UserCreate


class UserTestCase(UserCreate):
    """Тестирование представления пользователя"""

    def test_get_users(self):
        """Тестирование просмотра пользователей"""
        self.create_user()
        response = self.client.get('/users/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [{'email': 'example@test.ru',
              'tg_username': 'telegramtest',
              'name': None,
              'phone': None,
              'city': None,
              'avatar': None}]
        )

    def test_retrieve_user(self):
        """Тестирование просмотра одного пользователя"""
        self.create_user()
        response = self.client.get(f'/users/{self.user.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'email': 'example@test.ru',
             'tg_username': 'telegramtest',
             'name': None,
             'phone': None,
             'city': None,
             'avatar': None
             }
        )

    def test_update_user(self):
        """Тестирование обновления пользователя"""
        self.create_user()
        response = self.client.patch(f'/users/update/{self.user.id}/', {'email': 'newexample@sky.pro',
                                                                        'tg_username': 'newtelegram',
                                                                        'name': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'email': 'newexample@sky.pro',
             'tg_username': 'newtelegram',
             'name': 'test',
             'phone': None,
             'city': None,
             'avatar': None}
        )

    def test_delete_user(self):
        """Тестирование удаления пользователя"""
        self.create_user()
        response = self.client.delete(f'/users/delete/{self.user.pk}/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
