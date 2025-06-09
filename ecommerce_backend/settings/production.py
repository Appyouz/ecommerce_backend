from .base import * # Import all settings from base.py

DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
# ALLOWED_HOSTS will be read from environment variables (DJANGO_ALLOWED_HOSTS)
# in base.py, which will be provided by Render in production.
ALLOWED_HOSTS = [
    'ecommerce-backend-3rcr.onrender.com',
    # Add any other production hosts here
] + env.list('DJANGO_ALLOWED_HOSTS', default=[])
# DATABASES will be read from environment variables (DATABASE_URL)
# in base.py, which will be provided by Render in production.

# CORS settings for production frontend
# These will be read from environment variables (DJANGO_CORS_ALLOWED_ORIGINS)
# in base.py, which will be provided by Render in production.

# CSRF settings for production frontend
# These will be read from environment variables (DJANGO_CSRF_TRUSTED_ORIGINS)
# in base.py, which will be provided by Render in production.

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True # Redirect HTTP to HTTPS (Render handles HTTPS usually)
# CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE are True in base.py, which is good.
# CSRF_COOKIE_SAMESITE and SESSION_COOKIE_SAMESITE are 'None' in base.py which is fine for cross-site.
print("DEBUG: Current SECRET_KEY:", SECRET_KEY)
print("DEBUG: Current DATABASES:", DATABASES)
print("DEBUG: Current CORS_ALLOWED_ORIGINS:", CORS_ALLOWED_ORIGINS)
print("DEBUG: Using production settings.")
