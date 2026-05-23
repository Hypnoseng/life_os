from django.apps import AppConfig
from django.contrib.auth.models import User

class CoreConfig(AppConfig):
    name = 'core'

def create_superuser():
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "password123"
        )