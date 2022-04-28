from django.apps import AppConfig
from django.core import management
from .signals import populate_db

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(populate_db, sender=self)