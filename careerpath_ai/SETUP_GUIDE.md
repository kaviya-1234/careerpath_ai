# CareerPath AI — Django + SQLite3/MySQL Setup Guide

## Project Structure

```
your_project/
├── manage.py
├── your_project/          ← project config folder
│   ├── settings.py
│   ├── urls.py            ← add include() here
│   └── wsgi.py
├── assessment/            ← your app folder
│   ├── models.py          ✅ (use the new one provided)
│   ├── views.py           ✅ (use the new one provided)
│   ├── urls.py            ✅ (use the new one provided)
│   └── admin.py
└── templates/             ← HTML files go here
    ├── index.html         ✅ (use the new one provided)
    └── assessment.html    ✅ (use the new one provided)
```

---

## Step 1: Copy Files

1. Copy `models.py`, `views.py`, `urls.py` → into your `assessment/` app folder
2. Copy `index.html`, `assessment.html` → into your `templates/` folder

---

## Step 2: Update settings.py

### Database — Choose ONE:

**SQLite3 (easiest, no setup):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**MySQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerpath_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Add your app to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'assessment',   # ← your app name
]
```

### Set TEMPLATES DIRS:
```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],  # ← add this
        'APP_DIRS': True,
        ...
    },
]
```

---

## Step 3: Update project-level urls.py

```python
# your_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assessment.urls')),   # ← add this
]
```

---

## Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 5: For MySQL Only — create the database first

```sql
CREATE DATABASE careerpath_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON careerpath_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

Install driver:
```bash
pip install mysqlclient
# OR if mysqlclient fails:
pip install pymysql
```

If using pymysql, add to `your_project/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## Step 6: Run the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## What Changed from Old Code

| Before | After |
|--------|-------|
| localStorage for auth | Django session auth (secure) |
| localStorage for scores | MySQL/SQLite3 database |
| No backend save | All results saved to DB |
| `{% url 'assessment' %}` broken in index.html | Fixed with proper Django template tag |
| Signup created users in browser only | Users stored in Django's User model |

---

## API Endpoints (auto-created)

| URL | Method | Description |
|-----|--------|-------------|
| `/api/signup/` | POST | Register new user |
| `/api/login/` | POST | Login user |
| `/api/logout/` | GET | Logout user |
| `/api/auth-status/` | GET | Check if logged in |
| `/api/save/riasec/` | POST | Save RIASEC result |
| `/api/save/bigfive/` | POST | Save Big Five result |
| `/api/save/aptitude/` | POST | Save Aptitude result |
| `/api/save/academic/` | POST | Save Academic marks |
| `/api/save/ai-recommendation/` | POST | Save AI recommendation |
| `/api/results/` | GET | Get all saved results |
