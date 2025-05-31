# Бартерная система на Django

## Описание
Система для обмена товарами между пользователями с возможностью публикации объявлений и предложения обмена.

## Требования
- Python 3.8+
- pip (обычно устанавливается вместе с Python)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-репозиторий/barter.git
cd barter
```

2. Создайте и активируйте виртуальное окружение:

**Для Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Для Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка базы данных

1. Примените миграции:
```bash
python manage.py migrate
```

2. (Опционально) Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

## Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска сервер будет доступен по адресу:  
[http://localhost:8000](http://localhost:8000)  
Админ-панель: [http://localhost:8000/admin](http://localhost:8000/admin)

## Структура проекта

Основные приложения:
- `accounts` - управление пользователями и аутентификация
- `ads` - объявления и система обмена товарами

## Работа с файлами

1. Создайте необходимые директории:
```bash
mkdir static media
```

2. Для сбора статических файлов (в production):
```bash
python manage.py collectstatic
```

## Тестирование

Запуск всех тестов:
```bash
python manage.py test
```

Запуск тестов конкретного приложения:
```bash
python manage.py test apps.ads
```

Запуск с сохранением тестовой БД:
```bash
python manage.py test --keepdb
```

## Конфигурация

Основные настройки (`barter/settings.py`):
- Язык: Русский
- Часовой пояс: Москва (Europe/Moscow)
- База данных: SQLite (по умолчанию)
- Режим отладки: включен (DEBUG=True)

Для production необходимо:
1. Установить DEBUG=False
2. Добавить домен в ALLOWED_HOSTS
3. Настроить настоящую СУБД (PostgreSQL/MySQL)

## Зависимости

Основные используемые пакеты:
- Django 5.2.1
- django-mptt 0.17.0 (для древовидных структур)
- Pillow 11.2.1 (для работы с изображениями)

Полный список в файле `requirements.txt`
