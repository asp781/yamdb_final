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
git clone git@github.com:asp781/infra_sp2.git
```

```
cd /d/dev/infra_sp2/infra
```

Cоздать файл переменных окружения:

```
nano .env

```
## Шаблон наполнения файла:
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД 

Запустить docker-compose командой:

```
docker-compose up
```

Открываем новый термирал:

```
cd /d/dev/infra_sp2/infra
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```
Наполнить базу данных:

```
ddocker cp fixtures.json infra-web-1:app/
```
```
docker-compose exec web python manage.py loaddata fixtures.json
```
## Теперь проект доступен по адресу:
- http://localhost/api/v1/
- http://localhost/admin/

## Технологии:
- Python 3.8
- Django 2.2.19
- djangorestframework 3.12.4
- Docker
- NGINX
- GUNICORN
- POSTGRES

Автор проекта: [Алексей Спесивцев](https://github.com/asp781/)

https://github.com/asp781/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg