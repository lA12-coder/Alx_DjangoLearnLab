# api_project

A minimal Django + Django REST Framework starter project created by the assistant.

Quick start:

1. Create a virtual environment and activate it.

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
python -m pip install -r requirements.txt
```

3. Apply migrations and run server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

4. Visit the API endpoints:

- List view (DRF ListAPIView): `http://127.0.0.1:8000/api/books/`
- ViewSet routes (CRUD): `http://127.0.0.1:8000/api/books_all/`
