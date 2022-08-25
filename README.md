# Foodgram - «Продуктовый помощник»

---
![workflow](https://github.com/NColemann/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


### Адрес сервера
http://51.250.19.220/

## Описание
На сайте foodgram пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
1. Python 3.7
2. Django 2.2.16
3. Django REST framework 3.12.4
4. Docker
5. Nginx

### Зависимости
```
requests==2.26.0
django==2.2.16
djangorestframework==3.12.4
PyJWT==2.1.0
djangorestframework-simplejwt==5.1.0
django-filter==21.1
gunicorn==20.0.4
pytz==2020.1
asgiref==3.2.10
psycopg2-binary==2.9.3
sqlparse==0.3.1
python-dotenv==0.20.0
Pillow==9.2.0
django-colorfield==0.7.2
drf_extra_fields==3.4.0
djoser==2.1.0
```

### Шаблон наполнения файла .env

```yaml
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

### Запуск приложения в контейнерах
- Из директории проекта перейдите в директорию с файлом docker-compose и выполните команду:
```
cd infra
docker-compose up -d --build
```
- Выполните миграции
```
docker-compose exec web python manage.py migrate 
```
- Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Проект будет доступен по адресу: http://localhost:8080/


 ---

### Некоторые примеры запросов к API

#### Регистрация нового пользователя
POST /api/users/
```json
{
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}
```

#### Получение токена авторизации
POST /api/auth/token/login/
```json
{
  "password": "string",
  "email": "string"
}
```

#### Cписок рецептов
GET /api/recipes/

#### Создание рецепта
POST /api/recipes/
```json
{
  "ingredients": [
    {
      "id": "integer",
      "amount": "integer"
    }
  ],
  "tags": [
    "integer"
  ],
  "image": "data:image/png;base64",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}

#### Добавить рецепт в избранное
POST /api/recipes/{id}/favorite

#### Скачать список покупок
GET /api/recipes/download_shopping_cart/