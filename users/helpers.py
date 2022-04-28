from users.errors import NoValueError
from .models import User
import string
from django.contrib.auth.models import Permission


def clean_string(data, key, forbidden):
    try:
        dirty = data[key]
    except Exception as err:
        raise NoValueError(key)
    if dirty is None or dirty == '':
        raise NoValueError(key)
    return dirty.translate(str.maketrans('', '', forbidden)) # should we clean the string or throw an error ???

def create_user_with_role(data, role=5):
    email = clean_string(data, 'email', string.punctuation.replace('@', '').replace('.', ''))
    username = clean_string(data, 'username', string.punctuation)
    first_name = clean_string(data, 'first_name', string.punctuation)
    last_name = clean_string(data, 'last_name', string.punctuation)
    password = clean_string(data, 'password', '') # front should send an hash
    new = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password, role=role)
    new.save()
    return new

def permissions_for_superuser():
    # a superuser can do everything
    perm_read = Permission.objects.get( codename="can_read_user")
    perm_update = Permission.objects.get( codename="can_update_user")
    perm_delete = Permission.objects.get( codename="can_delete_user")
    perm_create_a_superuser = Permission.objects.get( codename="can_create_a_superuser")
    perm_create_an_org_admin = Permission.objects.get( codename="can_create_an_org_admin")
    perm_create_a_project_owner = Permission.objects.get( codename="can_create_a_project_owner")
    perm_create_an_org_member = Permission.objects.get( codename="can_create_an_org_member")
    perm_create_a_project_member = Permission.objects.get( codename="can_create_a_project_member")
    perm_create_comment = Permission.objects.get( codename="can_create_a_comment")
    perm_read_comments = Permission.objects.get( codename="can_read_all_the_comments")
    perm_update_comments = Permission.objects.get( codename="can_update_comments")
    perm_delete_comment = Permission.objects.get( codename="can_delete_comment")
    perm_create_organization = Permission.objects.get( codename="can_create_an_organization")
    perm_read_organization = Permission.objects.get( codename="can_read_all_the_organization")
    perm_update_organization = Permission.objects.get( codename="can_update_organization")
    perm_delete_organization = Permission.objects.get( codename="can_delete_organization")
    return [
            perm_create_a_superuser,
            perm_create_an_org_admin,
            perm_create_a_project_owner,
            perm_create_an_org_member,
            perm_create_a_project_member,
            perm_read,
            perm_update,
            perm_delete,
            perm_create_comment,
            perm_read_comments,
            perm_update_comments,
            perm_delete_comment,
            perm_create_organization,
            perm_read_organization,
            perm_update_organization,
            perm_delete_organization,
            ]

def permissions_for_org_admin():
    # a superuser can do everything
    perm_read = Permission.objects.get( codename="can_read_user")
    perm_update = Permission.objects.get( codename="can_update_user")
    perm_delete = Permission.objects.get( codename="can_delete_user")
    perm_create_an_org_admin = Permission.objects.get( codename="can_create_an_org_admin")
    perm_create_a_project_owner = Permission.objects.get( codename="can_create_a_project_owner")
    perm_create_an_org_member = Permission.objects.get( codename="can_create_an_org_member")
    perm_create_a_project_member = Permission.objects.get( codename="can_create_a_project_member")
    perm_create_comment = Permission.objects.get( codename="can_create_a_comment")
    perm_read_comments = Permission.objects.get( codename="can_read_all_the_comments")
    perm_update_comments = Permission.objects.get( codename="can_update_comments")
    perm_delete_comment = Permission.objects.get( codename="can_delete_comment")
    perm_read_organization = Permission.objects.get( codename="can_read_all_the_organization")
    perm_update_organization = Permission.objects.get( codename="can_update_organization")
    return [
            perm_create_an_org_admin,
            perm_create_a_project_owner,
            perm_create_an_org_member,
            perm_create_a_project_member,
            perm_read,
            perm_update,
            perm_delete,
            perm_create_comment,
            perm_read_comments,
            perm_update_comments,
            perm_delete_comment,
            perm_read_organization,
            perm_update_organization,
            ]

def permissions_for_org_member():
    # a superuser can do everything
    perm_read = Permission.objects.get( codename="can_read_user")
    perm_create_comment = Permission.objects.get( codename="can_create_a_comment")
    perm_read_comments = Permission.objects.get( codename="can_read_all_the_comments")
    perm_read_organization = Permission.objects.get( codename="can_read_all_the_organization")
    return [
            perm_read,
            perm_create_comment,
            perm_read_comments,
            perm_read_organization,
            ]

def permissions_for_proj_owner():
    # a superuser can do everything
    perm_read = Permission.objects.get( codename="can_read_user")
    perm_create_comment = Permission.objects.get( codename="can_create_a_comment")
    perm_read_comments = Permission.objects.get( codename="can_read_all_the_comments")
    perm_read_organization = Permission.objects.get( codename="can_read_all_the_organization")
    return [
            perm_read,
            perm_create_comment,
            perm_read_comments,
            perm_read_organization,
            ]

def permissions_for_proj_member():
    # a superuser can do everything
    perm_read = Permission.objects.get( codename="can_read_user")
    perm_create_comment = Permission.objects.get( codename="can_create_a_comment")
    perm_read_organization = Permission.objects.get( codename="can_read_all_the_organization")
    return [
            perm_read,
            perm_create_comment,
            perm_read_organization,
            ]