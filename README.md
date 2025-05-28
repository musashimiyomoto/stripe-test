# Stripe Test Shop

Тестовое задание - Django + Stripe API интеграция для обработки платежей.

## Описание

Веб-приложение для продажи товаров с интеграцией Stripe для обработки платежей. Поддерживает:

- Просмотр каталога товаров
- Покупка отдельных товаров
- Создание заказов из нескольких товаров
- Поддержка скидок и налогов
- Множественные валюты (USD, EUR, RUB)
- Админ-панель для управления товарами

## Функциональность

### Основные возможности:
- ✅ Django модель Item с полями (name, description, price, currency)
- ✅ API метод GET /buy/{id} для получения Stripe Session ID
- ✅ API метод GET /item/{id} для отображения страницы товара
- ✅ Stripe Checkout интеграция
- ✅ Docker поддержка
- ✅ Environment variables
- ✅ Django Admin панель

### Бонусные возможности:
- ✅ Модель Order для объединения товаров
- ✅ Модели Discount и Tax
- ✅ Поддержка множественных валют
- ✅ Красивый современный UI
- ✅ Полная интеграция с Stripe

## Технологии

- Python 3.11
- Django 5.2
- Stripe API
- PostgreSQL
- Docker & Docker Compose
- HTML/CSS/JavaScript

## Установка и запуск

### Вариант 1: Docker (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd stripe-test
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Заполните переменные окружения в `.env`:
```env
# Обязательные Stripe ключи
STRIPE_PUBLISHABLE_KEY=pk_test_ваш_публичный_ключ
STRIPE_SECRET_KEY=sk_test_ваш_секретный_ключ
```

4. Запустите приложение:
```bash
docker-compose up --build
```

5. Выполните миграции:
```bash
docker-compose exec web python manage.py migrate
```

6. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

7. Откройте браузер: http://localhost:8000

### Вариант 2: Локальная установка

1. Установите зависимости:
```bash
pip install poetry
poetry install
```

2. Настройте PostgreSQL и создайте базу данных

3. Создайте файл `.env` и заполните переменные

4. Выполните миграции:
```bash
poetry run python manage.py migrate
```

5. Создайте суперпользователя:
```bash
poetry run python manage.py createsuperuser
```

6. Запустите сервер:
```bash
poetry run python manage.py runserver
```

## Использование

### Админ-панель
- URL: http://localhost:8000/admin/
- Добавьте товары, скидки и налоги через админку

### API Endpoints

- `GET /` - Каталог товаров
- `GET /item/{id}/` - Страница товара с кнопкой покупки
- `GET /buy/{id}/` - Создание Stripe сессии для товара
- `GET /orders/` - Список заказов
- `GET /order/{id}/` - Детали заказа
- `GET /buy-order/{id}/` - Создание Stripe сессии для заказа
- `POST /add-to-order/{item_id}/` - Добавление товара в заказ

### Тестирование платежей

Используйте тестовые карты Stripe:
- Номер карты: `4242 4242 4242 4242`
- Срок действия: любая будущая дата
- CVC: любые 3 цифры

## Структура проекта

```
stripe-test/
├── core/                   # Основные настройки Django
├── payments/              # Приложение для платежей
│   ├── models.py         # Модели Item, Order, Discount, Tax
│   ├── views.py          # Views для обработки запросов
│   ├── admin.py          # Настройки админки
│   └── urls.py           # URL маршруты
├── templates/            # HTML шаблоны
├── docker-compose.yml    # Docker конфигурация
├── Dockerfile           # Docker образ
├── pyproject.toml       # Зависимости Python
└── README.md           # Документация
```

## Переменные окружения

Основные переменные в `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME=stripe-test
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

# Stripe (USD)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Stripe EUR (опционально)
STRIPE_PUBLISHABLE_KEY_EUR=pk_test_...
STRIPE_SECRET_KEY_EUR=sk_test_...

# Stripe RUB (опционально)
STRIPE_PUBLISHABLE_KEY_RUB=pk_test_...
STRIPE_SECRET_KEY_RUB=sk_test_...
```

## Особенности реализации

### Множественные валюты
Приложение поддерживает разные валюты через отдельные Stripe аккаунты. Для каждой валюты можно настроить свои ключи.

### Заказы
Пользователи могут добавлять товары в заказ и оплачивать их одной транзакцией. Заказы сохраняются в сессии.

### Скидки и налоги
Поддерживаются через Stripe Coupons и Tax Rates API.

## Разработка

### Создание миграций
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Сбор статических файлов
```bash
docker-compose exec web python manage.py collectstatic
```

### Логи
```bash
docker-compose logs web
```

## Лицензия

Тестовое задание для демонстрации навыков разработки.
