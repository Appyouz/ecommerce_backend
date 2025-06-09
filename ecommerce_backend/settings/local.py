from .base import * # Import all settings from base.py

# SECURITY WARNING: don't run with debug turned off in production!
DEBUG = True

# Allow all hosts for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]'] # Added IPv6 localhost

# Use SQLite database for local development. DATABASE_URL from .env will override this.
# If you comment this out, it will use the default from base.py, which is sqlite.
# If you want to use a local PostgreSQL for local dev, ensure DATABASE_URL is set in your .env.

# CORS settings for local frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # Next.js frontend local dev server
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# For local development, cookies might not need to be secure, or samesite strict
# unless local setup forces HTTPS (which is rare).
# However, for API-based authentication (JWTs), cookies might not be the primary concern.
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SAMESITE = 'Lax'
# CSRF_COOKIE_SAMESITE = 'Lax'

print("DEBUG: Using local settings.") # For debugging purposes
