"""
Base Django settings for ecommerce_backend project.
Contains settings common to both development and production.
"""
from pathlib import Path
import environ
from datetime import timedelta

# Initialize django-environ. It will automatically read from os.environ.
# We are NOT calling environ.Env.read_env() here, as environment variables
# should be provided by the OS/Docker for production and .env file for local.
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This BASE_DIR points to the root of your Django project (ecommerce_backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# Read SECRET_KEY from environment variables.
# Provide a dummy default for local development *only* if the env var isn't set.
# This default is NOT your production secret key and should NOT be used in production.
SECRET_KEY = env('SECRET_KEY', default='a-fallback-key-for-local-dev-only-do-not-use-in-production-or-ci-cd-F1nal')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters',

    'crispy_forms',
    'crispy_bootstrap4',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'pytest_django',

    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# These will be set based on environment variables (local/prod)
CORS_ALLOWED_ORIGINS = env.list('DJANGO_CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True # Keep this True for Django's session/CSRF cookies

CSRF_TRUSTED_ORIGINS = env.list('DJANGO_CSRF_TRUSTED_ORIGINS', default=[])


ROOT_URLCONF = 'ecommerce_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'ecommerce_backend' / 'templates', # Adjusted path for new structure
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_backend.wsgi.application'

# Database: Default to SQLite for simplicity if DATABASE_URL is not set (e.g., local dev without .env)
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# STATIC_ROOT must be an absolute path and where collectstatic gathers files.
STATIC_ROOT = BASE_DIR / 'staticfiles'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication', # Keep for Django Admin
        'rest_framework_simplejwt.authentication.JWTAuthentication', # For Bearer tokens
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Adjust per view if needed
    ),
}

REST_AUTH = {
    'USE_JWT': True,
    # Set JWT cookie settings to
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'REST_AUTH_JWT_AUTH_COOKIE_ACCESS': False, # Explicitly disable
    'REST_AUTH_JWT_AUTH_COOKIE_REFRESH': False, # Explicitly disable

    'LOGIN_VIEW': 'accounts.views.CustomLoginView',
    'LOGOUT_VIEW': 'accounts.views.CustomLogoutView',

    'OLD_PASSWORD_FIELD_ENABLED': True,
    'LOGOUT_GENERATE_TOKEN': True, # Important for JWT logout

    # CRUCIAL: Tell dj-rest-auth to use the JWTSerializer to output tokens in the body
    'SERIALIZERS': {
        'LOGIN_SERIALIZER': 'accounts.serializers.CustomJWTLoginSerializer',
        'TOKEN_SERIALIZER': 'dj_rest_auth.jwt_auth.serializers.JWTSerializer',
    },
}

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Standard Django session and CSRF cookie settings for cross-site
# These apply to sessionid and csrftoken, not JWTs
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'USER_ID_CLAIM': 'user_id',
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
}

ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_BY_EMAIL = True # Allow users to login by email
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1', 'password2']
ACCOUNT_LOGIN_METHODS = ['username', 'email']
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

# MEDIA FILES SETTINGS
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
