

def populateDB(sender, **kwargs):
    from django.contrib.auth.models import Permission
    from .models import User
    try:
        perm_read = Permission.objects.get( codename="can_read_user")
        perm_update = Permission.objects.get( codename="can_update_user")
        perm_delete = Permission.objects.get( codename="can_delete_user")
        perm_create_a_superuser = Permission.objects.get( codename="can_create_a_superuser")
        perm_create_an_org_admin = Permission.objects.get( codename="can_create_an_org_admin")
        perm_create_a_project_owner = Permission.objects.get( codename="can_create_an_project_owner")
        perm_create_an_org_member = Permission.objects.get( codename="can_create_an_org_member")
        perm_create_a_project_member = Permission.objects.get( codename="can_create_an_project_member")
        obj, create = User.objects.get_or_create( id=1, username='FAKEUSER', first_name= "FAKE USER", last_name= "placeholder", email= "NEVER@USE.FR", is_staff= True, is_active= False, date_joined= "2000-01-01T17:25:57.984Z", role=5)
        obj.save()
        obj, create = User.objects.get_or_create( id=2, username='BobKass', first_name= "Bob", last_name= "kass", email= "NEVER@USE.FR", is_staff= True, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=1)
        obj.user_permissions.set([
            perm_create_a_superuser,
            perm_create_an_org_admin,
            perm_create_a_project_owner,
            perm_create_an_org_member,
            perm_create_a_project_member,
            perm_read,
            perm_update,
            perm_delete
        ])
        obj.save()
        obj, create = User.objects.get_or_create( id=3, username='BenBill', first_name= "Ben", last_name= "Bill", email= "NEVER@USE.FR", is_staff= False, is_active= True, date_joined= "2000-01-01T17:25:57.984Z", role=2)
        obj.user_permissions.set([
            perm_create_a_superuser,
            perm_create_an_org_admin,
            perm_create_a_project_owner,
            perm_create_an_org_member,
            perm_create_a_project_member,
            perm_read,
            perm_update,
            perm_delete
        ])
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
    except Exception as err:
        print(err)