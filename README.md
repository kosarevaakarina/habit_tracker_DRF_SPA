###Трекер полезных привычек - бэкенд-часть SPA веб-приложения

_Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью
команд:_

```
python -m venv venv

source venv/bin/activate

pip install -r requirement.txt
```

_Для запуска приложения:_

```
python3 manage.py runserver
```

_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample_

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

_Для запуска celery_:

```
celery -A config beat --loglevel=info

celery -A config worker --loglevel=info
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

_В приложении есть следующие модели:_

* PleasantHabit (приятные привычки)
* GoodHabit (полезные привычки)
* User (пользователи)

В проекте есть интеграция Telegram Bot API, который рассылает пользователям привычки.
При создании модели GoodHabit создается периодическая задача, которая отправляет пользователю сообщение в Telegram в
конкретный
момент времени. Также есть периодическая задача, которая каждое утро рассылает пользователям задачи на день.

Документация проекта: http://127.0.0.1:8000/swagger/