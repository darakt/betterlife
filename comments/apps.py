from django.apps import AppConfig
from .signals import populate_db
def populate_db(sender, **kwargs):
    from users.models import User
    from .models import Comment
    creator, create = User.objects.get_or_create( id=1, username='FAKEUSER', first_name= "FAKE USER", last_name= "placeholder", email= "NEVER@USE.FR", is_staff= True, is_active= False, date_joined= "2000-01-01T17:25:57.984Z", role=5)
    obj, create = Comment.objects.get_or_create(id=1, title='placeholder', text='< This comment was deleted >', written_by=creator, in_response_to=None)

class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(populate_db, sender=self)
