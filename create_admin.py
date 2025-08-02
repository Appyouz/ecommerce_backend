import os
import sys
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

def create_admin():
    try:
        User = get_user_model()
    except Exception as e:
        print(f"Failed to get user model: {e}")
        return

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not password:
        print("DJANGO_SUPERUSER_PASSWORD environment variable is not set. Cannot create superuser.")
        return

    try:
        User.objects.get(username=username)
        print(f"Superuser '{username}' already exists. Skipping.")
    except ObjectDoesNotExist:
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created. REMEMBER TO CHANGE THE PASSWORD.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Production")
    django.setup()
    create_admin()
