from django.apps import AppConfig
from django.core import management

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        from users.models import User
        try:
            obj, create = User.objects.get_or_create( id=1, username='PLACEHOLDER', first_name= "THIS IS A", last_name= "placeholder", email= "NEVER@USE.FR", is_staff= True, is_active= False, date_joined= "2000-01-01T17:25:57.984Z")
            # here we are creating an object with an id, messing the sequence used for the id, we need to do an empty migrations then use it to alter the sequence
        except Exception as err:
            print(err)