import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FixWatt.settings')
django.setup()

from django.contrib.auth.models import User

username = 'testuser_manual'
password = 'StrongPassword123!'
email = 'testuser_manual@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, email=email, password=password, first_name='Test', last_name='Manual')
    print(f"User {username} created.")
else:
    print(f"User {username} already exists.")
