from django.apps import AppConfig
from .signals import populate_db

class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organizations'
    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(populate_db, sender=self)
