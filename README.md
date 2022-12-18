# Сервис Foodgram

![foodgram_workflow](https://github.com/Rinko69/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
http://158.160.14.164:80
____


## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

____

## Описание проекта

Foodgram это ресурс для публикации рецептов.  
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в pdf формате

## Установка проекта локально:

### Клонировать репозиторий:
```python
    git clone git@github.com:Rinko69/foodgram-project-react.git
```
### Cоздать и активировать виртуальное окружение:

```python
python -m venv env
```

```python
source env/bin/activate
```

### Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=username # логин для подключения к базе данных
- POSTGRES_PASSWORD=password # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД
```
### Перейти в директирию и установить зависимости из файла requirements.txt:

```python
cd backend/
pip install -r requirements.txt
```

### Выполните миграции:

```python
python manage.py migrate
```

### Запустите сервер:
```python
python manage.py runserver
```

## Запуск проекта в Docker контейнере:

### Установите Docker:

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

### Запустите docker compose:
```python
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **backend**
  > 3. контейнер web-сервера **nginx**
### Примените миграции:
```python
docker-compose exec backend python manage.py migrate
```
### Загрузите ингредиенты:
```python
docker-compose exec backend python manage.py load_ingrs
```
### Загрузите теги:
```python
docker-compose exec backend python manage.py load_tags
```
### Создайте администратора:
```python
docker-compose exec backend python manage.py createsuperuser
```
### Соберите статику:
```python
docker-compose exec backend python manage.py collectstatic --noinput
```

**Теперь проект готов к работе и доступен по адресу http://158.160.14.164:80.
И также доступен доступ к админке: http://158.160.14.164/admin/.**
____

## Руководство к проекту:
### Пользовательские роли:
- Гость — может просматривать рецепты.
- Аутентифицированный пользователь (user) — может читать всё, как и Гость, может публиковать рецепты, может добавлять рецепты в избранное, может подписываться на других пользователей; может редактировать и удалять свои рецепты, может создавать и скачивать список покупок на основе избранных рецептов. Эта роль присваивается по умолчанию каждому новому пользователю.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора.

### Алгоритм регистрации пользователей:
- Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис Foodgram отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.

### Создание пользователя администратором:
Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая — в документации).
В этот момент письмо с кодом подтверждения пользователю отправлять не нужно. После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.
____

## Ресурсы сервиса API Foodgram:
- auth: аутентификация.
- users: пользователи.
- recipes: рецепты.
- tags: тэги (ключевые слова).
- following: список избранного.
- shopping_list: список покупок.
