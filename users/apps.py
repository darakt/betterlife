from django.apps import AppConfig
from django.core import management
from .signals import populateDB

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(populateDB, sender=self)