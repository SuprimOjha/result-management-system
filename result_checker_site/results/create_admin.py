import os
import django

# Set environment variable for settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'result_checker.settings')  # ← matches your project name
django.setup()

from django.contrib.auth.models import User

# create superuser if not exists
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="suprimojha25@gmail.com",
        password=os.environ.get("ADMIN_PASSWORD", "12345678")  # use env var if possible
    )
    print("Admin user created!")
else:
    print("Admin user already exists.")