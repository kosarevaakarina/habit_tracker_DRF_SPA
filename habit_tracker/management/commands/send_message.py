from django.core.management import BaseCommand

from habit_tracker.tasks import send_all_tracker


class Command(BaseCommand):
    """Отправка сообщения пользователю от телеграм-бота, в теле письма указаны все полезные привычки, которые
    необходимо сделать за день"""

    def handle(self, *args, **options):
        try:
            send_all_tracker()
        except Exception:
            raise 'Рассылка не существует'
