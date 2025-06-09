import os

# Get the DJANGO_ENV environment variable, default to 'development' if not set
SETTINGS_MODULE = os.environ.get('DJANGO_ENV', 'development')

if SETTINGS_MODULE == 'production':
    from .production import *
    print("Loading production settings...")
elif SETTINGS_MODULE == 'development':
    from .local import *
    print("Loading local development settings...")
else:
    # Fallback to local settings if DJANGO_ENV is set to something unexpected
    from .local import *
    print(f"WARNING: Unknown DJANGO_ENV '{SETTINGS_MODULE}'. Loading local development settings.")
