import os
from pathlib import Path
from random import randint

import sentry_sdk
from dotenv import load_dotenv
from rich.console import Console
from sentry_sdk.integrations.django import DjangoIntegration


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "mykytaso.com",
    "www.mykytaso.com",
]


# CSRF settings
# Only use secure cookies in production (when DEBUG is False)
CSRF_COOKIE_SECURE = not DEBUG
CSRF_TRUSTED_ORIGINS = [
    "https://mykytaso.com",
    "https://*.mykytaso.com",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # Third-party apps
    "users",
    "posts",
    "likes",
    "django_recaptcha",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middleware.RequestLoggingMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "html"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


AUTH_USER_MODEL = "users.User"

# Sites framework
SITE_ID = 1


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Login/Logout redirect URLs
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "user_profile"
LOGOUT_REDIRECT_URL = "login"

SESSION_COOKIE_AGE = 86400 * 14  # 14 days in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Do not expire session on browser close
SESSION_SAVE_EVERY_REQUEST = False  # Do not extend session on every request

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "frontend/static",
]


# To prevent browsers from serving outdated cached CSS after deployment.
STYLES_HASH = os.getenv("GITHUB_SHA") or str(randint(1, 10000))  # noqa: S311


# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Email Configuration (Mailgun)
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_URL = os.getenv("MAILGUN_API_URL", "https://api.mailgun.net/v3")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@yourdomain.com")
SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

# Email Verification Settings
EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = 24

# Password Reset Settings
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour in seconds

# Logging Configuration
RICH_CONSOLE = Console(width=260, force_terminal=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # Handlers control where log messages go.
    "handlers": {
        "console": {
            "()": "rich.logging.RichHandler",  # Rich handler for colorized output.
            "console": RICH_CONSOLE,  # Wide console to prevent line wrapping.
            "rich_tracebacks": True,  # Format exceptions using Rich's Traceback class.
            "show_path": False,  # Hide file path column to prevent narrow wrapping.
            "omit_repeated_times": True,
        },
    },
    # The root logger is the catch-all at the top of the logger hierarchy. Any logger that doesn't match a specific entry in "loggers" (and has propagate=True, the default) will bubble up to here.
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,  # Stops Django logs from also reaching the root logger. Without this, every Django log message would be printed twice (once by this logger's console handler, once by root's console handler).
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",  # Only log 5xx errors; 4xx are already covered by RequestLoggingMiddleware.
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "WARNING",  # Suppress default request logs; already covered by RequestLoggingMiddleware.
            "propagate": False,
        },
        "request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Sentry Configuration
SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN and not DEBUG:
    # activate sentry on production
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],
    )

# reCAPTCHA Configuration
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")

# For local testing without real credentials
if DEBUG:
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
