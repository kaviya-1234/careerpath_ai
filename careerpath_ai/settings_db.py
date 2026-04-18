# ============================================================
#  settings.py  — DATABASE CONFIGURATION
#  Add this to your existing settings.py
#  Choose ONE option below (SQLite3 OR MySQL)
# ============================================================

# ── OPTION 1: SQLite3 (No setup needed — works out of the box) ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── OPTION 2: MySQL ──────────────────────────────────────────
# Comment out Option 1 above and uncomment this block
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'careerpath_db',
#         'USER': 'your_mysql_username',
#         'PASSWORD': 'your_mysql_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# ── INSTALLED APPS — make sure your app is listed ────────────
# Add your app name (e.g. 'assessment') to INSTALLED_APPS:
#
# INSTALLED_APPS = [
#     ...
#     'assessment',   # <-- your app name here
# ]

# ── TEMPLATES — make sure Django finds your HTML files ────────
# In your TEMPLATES setting, set DIRS to:
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],   # <-- add this
#         'APP_DIRS': True,
#         ...
#     },
# ]
