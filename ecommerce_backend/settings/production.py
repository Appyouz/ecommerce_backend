from .base import * # Import all settings from base.py

DEBUG = False

# ALLOWED_HOSTS will be read from environment variables (DJANGO_ALLOWED_HOSTS)
# in base.py, which will be provided by Render in production.
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

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

#Cloudinary configurations
CLOUDINARY_CLOUD_NAME = env.list('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = env.list('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = env.list('CLOUDINARY_API_SECRET')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


print("DEBUG: Using production settings.")
