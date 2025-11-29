import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_eai.settings')
django.setup()

User = get_user_model()
try:
    user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    user.set_password('admin')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("User 'admin' password set to 'admin'.")
except Exception as e:
    print(f"Error: {e}")
