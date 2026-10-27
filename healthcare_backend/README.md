# Healthcare Backend API

A Django REST Framework + PostgreSQL healthcare API with JWT authentication, patient and doctor CRUD, patient-doctor assignments, validation, ownership checks, and automated API tests.

## Features

- Email-based registration and login; passwords are hashed by Django.
- JWT access and refresh tokens using `djangorestframework-simplejwt`.
- Patients are private to the account that created them.
- Doctors are visible to authenticated users; only the doctor creator can update/delete a doctor record.
- A user can assign doctors only to their own patients.
- Prevents duplicate patient-doctor assignments.
- PostgreSQL configuration is environment-driven.
- Consistent JSON error responses from DRF validation and permissions.
- Django admin and automated tests.

## 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+ **or** Docker Desktop / Docker Engine with Compose

## 2. Install

### Windows PowerShell

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY` and database credentials. Never commit `.env`.

## 3. Start PostgreSQL

The simplest option is Docker Compose. Run this from the project root **after** creating `.env`:

```bash
docker compose up -d db
```

If using a locally installed PostgreSQL server, create a database/user matching `.env` and ensure the server is running.

## 4. Migrate and run

```bash
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/`

> The repository intentionally does not include generated migration files, so `makemigrations` is needed once before `migrate`.

## Authentication

### Register

`POST /api/auth/register/`

```json
{
  "name": "Anuj Verma",
  "email": "anuj@example.com",
  "password": "StrongPassword123!"
}
```

Returns the created user and JWT access/refresh tokens.

### Login

`POST /api/auth/login/`

```json
{
  "email": "anuj@example.com",
  "password": "StrongPassword123!"
}
```

### Refresh token

`POST /api/auth/token/refresh/`

```json
{ "refresh": "YOUR_REFRESH_TOKEN" }
```

For protected routes, send:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API endpoints

All patient, doctor, and mapping endpoints require a valid access token.

| Method | Endpoint | Behavior |
|---|---|---|
| POST | `/api/auth/register/` | Register account |
| POST | `/api/auth/login/` | Login and return JWTs |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/patients/` | Create patient |
| GET | `/api/patients/` | List your patients only |
| GET | `/api/patients/<id>/` | Retrieve your patient |
| PUT/PATCH | `/api/patients/<id>/` | Update your patient |
| DELETE | `/api/patients/<id>/` | Delete your patient |
| POST | `/api/doctors/` | Create doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Retrieve doctor |
| PUT/PATCH | `/api/doctors/<id>/` | Update doctor (creator only) |
| DELETE | `/api/doctors/<id>/` | Delete doctor (creator only) |
| POST | `/api/mappings/` | Assign doctor to your patient |
| GET | `/api/mappings/` | List mappings for your patients |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to your patient |
| DELETE | `/api/mappings/<mapping_id>/` | Remove a mapping for your patient |

`PATCH` is also supported for partial updates. For the assignment's specified mapping URL shape, `GET /api/mappings/<id>/` interprets the ID as a **patient ID**, while `DELETE` interprets it as a **mapping ID**.

### Patient payload

```json
{
  "name": "Patient Name",
  "age": 35,
  "gender": "female",
  "phone": "+91-9876543210",
  "address": "Delhi NCR",
  "medical_history": "Optional notes"
}
```

`gender`: `male`, `female`, `other`, or `prefer_not_to_say`.

### Doctor payload

```json
{
  "name": "Dr. Example",
  "specialization": "Cardiology",
  "email": "doctor@example.com",
  "phone": "+91-9876543210",
  "experience_years": 8,
  "clinic_address": "Delhi NCR"
}
```

### Assign a doctor

`POST /api/mappings/`

```json
{
  "patient": 1,
  "doctor": 1
}
```

## Postman quick start

1. Register or log in and copy `access`.
2. In Postman, set Authorization type to **Bearer Token** and paste the access token.
3. Send requests to the endpoints above with JSON bodies and `Content-Type: application/json`.
4. Test authorization by logging in as a second user and trying to access the first user's patient IDs; these should return `404`.

## Run tests

```bash
python manage.py test
```

Tests use Django's test database configuration. For full integration testing against PostgreSQL, ensure the PostgreSQL database user can create test databases.

## Production notes

- Set `DEBUG=False`, a secure random `SECRET_KEY`, and explicit `ALLOWED_HOSTS`.
- Use HTTPS and secure deployment secrets.
- Configure PostgreSQL backups, monitoring, and restricted network access.
- Configure production `CSRF_TRUSTED_ORIGINS`, logging, rate limiting, and email-based password recovery before production use.
- This is an educational starter project, not a certified clinical-record system. Do not put real patient data into a public demo.
