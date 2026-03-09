# results/create_admin.py
from django.contrib.auth.models import User
import django
import os

# Setup Django settings so this script can run independently
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'result_checker.settings')
django.setup()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="suprimojha25@gmail.com",
        password="hello@12345"
    )
    print("Admin user created")
else:
    print("Admin already exists")