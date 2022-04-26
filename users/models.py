from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
import json

attributeWhiteListed = [ # we don't want to pass everything to the front so no need to jsonified everything
    'id',
    'username',
    'first_name',
    'last_name',
    'email',
    'date_joined'
]

def get_deleted_comment():
    pass

def get_placeholder_for_deleted_comment():
    return User.objects.get_or_create(id=1)

class User(AbstractUser):
    superuser = 1
    organization_admin = 2
    organization_member = 3
    project_owner = 4
    project_member = 5

    roles = (
        (superuser, 'superuser'),
        (organization_admin, 'organization admin'),
        (organization_member, 'organization member'),
        (project_owner, 'project owner'),
        (project_member, 'project member'),
    )
    role = models.PositiveSmallIntegerField(choices=roles, default=5)
    def toJson(self):
        jsonified = {}
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None and key in attributeWhiteListed and self.__dict__[key] != '':
                # print('[{}] = {}'.format(key, self.__dict__[key]))
                jsonified[key] = self.__dict__[key]
        return jsonified
    class Meta:
        permissions = [
                ('can_create_user', 'can create user'),
                ('can_read_user','can read user'),
                ('can_update_user', 'can update user'),
                ('can_delete_user', 'can delete user')
                ]