import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'result_checker.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = os.environ.get("ADMIN_PASSWORD", "1234")  # fallback if not set
email = "suprimojha25@gmail.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Admin user created!")
else:
    print("Admin user already exists!")