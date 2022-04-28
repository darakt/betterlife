

def populate_db(sender, **kwargs):
    from django.contrib.auth.models import Permission
    from users.models import User
    from .models import Organization

    try:
        perm_create = Permission.objects.get( codename="can_create_an_organization")
        perm_read = Permission.objects.get( codename="can_read_all_the_organization")
        perm_update = Permission.objects.get( codename="can_update_organization")
        perm_delete = Permission.objects.get( codename="can_delete_organization")
        obj, create = User.objects.get_or_create( id=1, username='FAKEUSER', first_name= "FAKE USER", last_name= "placeholder", email= "NEVER@USE.FR", is_staff= True, is_active= False, date_joined= "2000-01-01T17:25:57.984Z", role=5)
        obj.save()
        creator, create = User.objects.get_or_create( id=2, username='BobKass', first_name= "Bob", last_name= "kass", email= "NEVER@USE.FR", is_staff= True, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=1)
        creator.user_permissions.add(perm_create)
        creator.user_permissions.add(perm_read)
        creator.user_permissions.add(perm_update)
        creator.user_permissions.add(perm_delete)
        creator.save()
        obj, create = User.objects.get_or_create( id=3, username='BenBill', first_name= "Ben", last_name= "Bill", email= "NEVER@USE.FR", is_staff= False, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=2)
        obj.user_permissions.add(perm_create)
        obj.user_permissions.add(perm_read)
        obj.user_permissions.add(perm_update)
        obj.user_permissions.add(perm_delete)
        obj.save()
        obj, create = User.objects.get_or_create( id=4, username='MadelinePros', first_name= "Madeline", last_name= "Pross", email= "NEVER@USE.FR", is_staff= False, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=3)
        obj.user_permissions.add(perm_read)
        obj.save()
        obj, create = User.objects.get_or_create( id=5, username='TheoGolden', first_name= "Theo", last_name= "Golden", email= "NEVER@USE.FR", is_staff= False, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=4)
        obj.user_permissions.add(perm_read)
        obj.save()
        obj, create = User.objects.get_or_create( id=6, username='LeaPri', first_name= "Lea", last_name= "Pri", email= "NEVER@USE.FR", is_staff= False, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=5)
        obj.user_permissions.add(perm_read)
        obj.save()
        obj, create = Organization.objects.get_or_create(id=1, name='betterlife', description='Our goal is betterlife', language='aa')
        obj.save()
        obj.admins.add(creator)
    except Exception as err:
        print(err)