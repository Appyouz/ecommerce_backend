import os
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def create_admin_user():
    """
    Creates a superuser programmatically.
    This script should be used for one-off deployments and deleted afterwards.
    """
    if User.objects.filter(username='admin').exists():
        print("Admin user already exists. Skipping.")
        return

    # Use a secure, temporary password. You must change this immediately!
    temp_password = os.environ.get('DJANGO_SUPERUSER_TEMP_PASSWORD', 'temp_password_1234')
    
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=temp_password
        )
        print("Superuser 'admin' created successfully with a temporary password.")
        print("Please log in to your Django Admin and change this password immediately!")
    except Exception as e:
        print(f"Failed to create superuser: {e}")

if __name__ == '__main__':
    # Ensure Django settings are configured before running
    # This is not strictly necessary if called from a manage.py command
    # but good practice for standalone scripts.
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
        os.environ.setdefault('DJANGO_CONFIGURATION', 'production')

    create_admin_user()
