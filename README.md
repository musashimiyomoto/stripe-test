# Stripe Test Shop

Test Assignment – Django + Stripe API integration for payment processing.

## Description

A web application for selling products with Stripe integration for payment processing. Supports:

* Product catalog browsing
* Purchasing individual items
* Creating orders with multiple items
* Discounts and taxes support
* Multiple currencies (USD, EUR, RUB)
* Admin panel for product management

## Functionality

### Core Features:

* ✅ Django `Item` model with fields (name, description, price, currency)
* ✅ `GET /buy/{id}` API endpoint to retrieve a Stripe Session ID
* ✅ `GET /item/{id}` API endpoint to display a product page
* ✅ Stripe Checkout integration
* ✅ Docker support
* ✅ Environment variables configuration
* ✅ Django Admin panel

### Bonus Features:

* ✅ `Order` model for grouping items
* ✅ `Discount` and `Tax` models
* ✅ Multi-currency support
* ✅ Modern, clean UI
* ✅ Full Stripe integration

## Technologies

* Python 3.11
* Django 5.2
* Stripe API
* PostgreSQL
* Docker & Docker Compose
* HTML/CSS/JavaScript

## Installation & Setup

### Option 1: Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd stripe-test
```

2. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

3. Fill in the environment variables in `.env`:

```env
# Required Stripe keys
STRIPE_PUBLISHABLE_KEY=pk_test_your_public_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
```

4. Start the application:

```bash
docker-compose up --build
```

5. Run migrations:

```bash
docker-compose exec web python manage.py migrate
```

6. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

7. Open in browser: [http://localhost:8000](http://localhost:8000)

---

### Option 2: Local Setup

1. Install dependencies:

```bash
pip install poetry
poetry install
```

2. Configure PostgreSQL and create a database

3. Create a `.env` file and fill in environment variables

4. Run migrations:

```bash
poetry run python manage.py migrate
```

5. Create a superuser:

```bash
poetry run python manage.py createsuperuser
```

6. Start the server:

```bash
poetry run python manage.py runserver
```

---

## Usage

### Admin Panel

* URL: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Add products, discounts, and taxes via the admin interface

### API Endpoints

* `GET /` – Product catalog
* `GET /item/{id}/` – Product page with purchase button
* `GET /buy/{id}/` – Create Stripe session for a product
* `GET /orders/` – List of orders
* `GET /order/{id}/` – Order details
* `GET /buy-order/{id}/` – Create Stripe session for an order
* `POST /add-to-order/{item_id}/` – Add item to order

---

## Payment Testing

Use Stripe test cards:

* Card number: `4242 4242 4242 4242`
* Expiration date: any future date
* CVC: any 3 digits

---

## Project Structure

```
stripe-test/
├── core/                   # Main Django settings
├── payments/               # Payments application
│   ├── models.py           # Models: Item, Order, Discount, Tax
│   ├── views.py            # Request handling views
│   ├── admin.py            # Admin configuration
│   └── urls.py             # URL routes
├── templates/              # HTML templates
├── docker-compose.yml      # Docker configuration
├── Dockerfile              # Docker image
├── pyproject.toml          # Python dependencies
└── README.md               # Documentation
```

---

## Environment Variables

Main variables in `.env`:

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

# Stripe EUR (optional)
STRIPE_PUBLISHABLE_KEY_EUR=pk_test_...
STRIPE_SECRET_KEY_EUR=sk_test_...

# Stripe RUB (optional)
STRIPE_PUBLISHABLE_KEY_RUB=pk_test_...
STRIPE_SECRET_KEY_RUB=sk_test_...
```

---

## Implementation Details

### Multiple Currencies

The application supports multiple currencies using separate Stripe accounts. Each currency can have its own API keys.

### Orders

Users can add multiple items to an order and pay in a single transaction. Orders are stored in the session.

### Discounts and Taxes

Implemented using Stripe Coupons and Tax Rates API.

---

## Development

### Creating Migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Collecting Static Files

```bash
docker-compose exec web python manage.py collectstatic
```

### Logs

```bash
docker-compose logs web
```

---

## License

Test assignment created to demonstrate development skills.
