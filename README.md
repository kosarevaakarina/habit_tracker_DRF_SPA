# Трекер полезных привычек - бэкенд-часть SPA веб-приложения
## Описание
* Настроен CORS.
* Настроена интеграция с Telegram.
* Реализована пагинация (с выводом по 5 привычек на страницу).
* Реализованы валидаторы:
  * Исключить одновременный выбор связанной привычки и указания вознаграждения.
  * Время выполнения должно быть не больше 120 секунд.
  * В связанные привычки могут попадать только привычки с признаком приятной привычки.
  * У приятной привычки не может быть вознаграждения или связанной привычки.
  * Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
* Описаны права доступа:
    * Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.
    * Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.
* Настроена отложенная задача через Celery.
* Имеется список зависимостей.
* Результат проверки Flake8 равен 100%, при исключении миграций.
* Эндпоинты:
  * Регистрация и авторизация пользователя
  * Список привычек текущего пользователя с пагинацией
  * Список публичных привычек
  * Создание, редкатирование и удаление привычки
## Технологии
* Python
* Django, DRF
* JWT, DRF-YASG
* PostgreSQL
* Celery, Redis
* TelegramBotApi
## Сущности
* Приятные привычки
* Полезные привычки
* Пользователь
---
### Запуск проекта в Docker:
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.example:_
```
#Email
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

#Celery
CELERY_BROKER_URL=redis://redis_habit:6379
CELERY_RESULT_BACKEND=redis://redis_habit:6379

#Telegram bot
TELEGRAM_BOT_API=

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST='db_habit'
POSTGRES_PORT=5432
POSTGRES_HOST_AUTH_METHOD=trust

#Secret key
SECRET_KEY=
```
_Для создания образа из Dockerfile и запуска контейнера запустить команду:_
```
docker-compose up --build
```
_или_
```
docker-compose up -d --build
```
_Второй вариант для запуска в фоновом режиме._

### Запуск приложения в локальной сети:
_Для запуска проекта необходимо клонировать репозиторий и создать и активировать виртуальное окружение:_ 
```
python3 -m venv venv

source venv/bin/activate
```
_Установить зависимости:_
```
pip install -r requirements.txt
```
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample:_
```
#Email
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

#Celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

#Telegram bot
TELEGRAM_BOT_API=

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

#Secret key
SECRET_KEY=
```
_Выполнить миграции:_
```
python3 manage.py migrate
```
_Для заполнения БД запустить команду:_

```
python3 manage.py fill
```

_Для создания администратора запустить команду:_

```
python3 manage.py csu
```

_Для заполнения БД запустить команду:_

```
python3 manage.py fill
```

_Для запуска redis_:

```
redis-cli
```

_Для запуска celery:_

```
celery -A config worker --loglevel=info
```

_Для запуска django-celery-beat:_

```
celery -A config beat --loglevel=info
```

_Для запуска приложения:_

```
python3 manage.py runserver
```

_Для отправки пользователю сообщения со всеми задачами на день, запустить команду:_

```
python3 manage.py send_message
```

_Для тестирования проекта запустить команду:_

```
python3 manage.py test
```

_Для запуска подсчета покрытия и вывода отчет запустить команды:_

```
coverage run --source='.' manage.py test

coverage report
```


Документация проекта: http://127.0.0.1:8000/swagger/
