# Money Map

MoneyMap is a personal finance management API built with Django and Django REST Framework.
The project allows users to manage wallets, categories, transactions, and budgets.

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL / SQLite
* Simple JWT
* drf-spectacular
* pytest
* Render

## Features

* User authentication
* Wallet management
* Income and expense categories
* Transaction tracking
* Budget management
* Admin panel
* REST API structure
* Swagger documentation

## API Documentation

Interactive documentation:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

Detailed endpoint list:

- [API Endpoints](docs/API.md)
- [Authentication Guide](docs/AUTH.md)

## Installation

Clone the repository:

```bash
git clone https://github.com/y-kondrashova/money_map_api.git
cd money_map_api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

## Running Tests

```bash
pytest
```

## Static Files

Collect static files with:

```bash
python manage.py collectstatic --no-input
```

The generated `staticfiles/` folder should not be committed to Git.

## Deployment

The project is prepared for deployment on Render.

Production environment variables:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=your-render-postgresql-database-url
WEB_CONCURRENCY=4
```

Build command:

```bash
./build.sh
```

Start command example:

```bash
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

## Project Structure

```text
money_map_api/
├── manage.py
├── requirements.txt
├── build.sh
├── README.md
├── .env.example
├── docs/
├── templates/
├── tests/
└── config/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    ├── wsgi.py
    └── apps/
        ├── accounts/
        ├── budgets/
        ├── category/
        ├── transactions/
        └── wallets/
```

## License

This project is for educational and portfolio purposes.
