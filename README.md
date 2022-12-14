# Проект YaMDb
#### Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку, из которых формируется рейтинг.


####  Как запустить проект:
```
cd /d/dev
```

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:asp781/yamdb_final.git

```
## Создать переменные окружения в разделе `secrets` настроек текущего репозитория:

- DOCKER_PASSWORD # Пароль от Docker Hub
- DOCKER_USERNAME # Логин от Docker Hub
- HOST # Публичный ip адрес сервера
- USER # Пользователь зарегистрированный на сервере
- PASSPHRASE # Если ssh-ключ защищен фразой-паролем
- SSH_KEY # Приватный ssh-ключ
- TELEGRAM_TO # ID телеграм-аккаунта
- TELEGRAM_TOKEN # Токен бота

- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД 

Выполнить миграции:

```
sudo docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
sudo docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Наполнить базу данных:

```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
## Теперь проект доступен по адресу:
- http://asp781.ddns.net/api/v1/
- http://asp781.ddns.net/admin/

## После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.

## Технологии:
- Python 3.8
- Django 2.2.19
- djangorestframework 3.12.4
- Docker
- NGINX
- GUNICORN
- POSTGRES

Автор проекта: [Алексей Спесивцев](https://github.com/asp781/)

![yamdb_workflow](https://github.com/asp781/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)