from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from users.models import User
from users.errors import GenericError, NoValueError
from django.db import IntegrityError
from django.http import JsonResponse
from users.helpers import create_user_with_role
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
import json
import string
import ast

allowed_to_update = ['username', 'first_name', 'last_name', 'email', 'id'] #TODO: should be an env var

def status():
    return HttpResponse('UP')

@csrf_exempt
def create(request): # add mandatory fields (name, ...) + here we are using form data
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=5)
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

@csrf_exempt
def createSuperuser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=1)
            # a superuser can do everything
            perm_read = Permission.objects.get( codename="can_read_user")
            perm_update = Permission.objects.get( codename="can_update_user")
            perm_delete = Permission.objects.get( codename="can_delete_user")
            perm_create_a_superuser = Permission.objects.get( codename="can_create_a_superuser")
            perm_create_an_org_admin = Permission.objects.get( codename="can_create_an_org_admin")
            perm_create_a_project_owner = Permission.objects.get( codename="can_create_an_project_owner")
            perm_create_an_org_member = Permission.objects.get( codename="can_create_an_org_member")
            perm_create_a_project_member = Permission.objects.get( codename="can_create_an_project_member")
            new.user_permissions.set([perm_create_a_superuser, perm_create_an_org_admin, perm_create_a_project_owner, perm_create_an_org_member, perm_create_a_project_member,perm_read, perm_update, perm_delete])
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

@csrf_exempt
def createOrgAdmin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=2)
            perm_read = Permission.objects.get( codename="can_read_user")
            perm_update = Permission.objects.get( codename="can_update_user")
            perm_delete = Permission.objects.get( codename="can_delete_user")
            perm_create_a_superuser = Permission.objects.get( codename="can_create_a_superuser")
            perm_create_an_org_admin = Permission.objects.get( codename="can_create_an_org_admin")
            perm_create_a_project_owner = Permission.objects.get( codename="can_create_an_project_owner")
            perm_create_an_org_member = Permission.objects.get( codename="can_create_an_org_member")
            perm_create_a_project_member = Permission.objects.get( codename="can_create_an_project_member")
            new.user_permissions.set([perm_create_a_superuser, perm_create_an_org_admin, perm_create_a_project_owner, perm_create_an_org_member, perm_create_a_project_member,perm_read, perm_update, perm_delete])
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

@csrf_exempt
def createOrgMember(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=3)
            perm_read = Permission.objects.get( codename="can_read_user")
            new.user_permissions.set([perm_read])
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

@csrf_exempt
def createProjOwner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=4)
            perm_read = Permission.objects.get( codename="can_read_user")
            new.user_permissions.set([perm_read])
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })


@csrf_exempt
def createProjMember(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            new = create_user_with_role(data=data, role=5)
            perm_read = Permission.objects.get( codename="can_read_user")
            new.user_permissions.set([perm_read])
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

def getAUser(request, id = 0): # through ID | id = 0, bad idea?
    if request.method == 'GET':
        try:
            if id == 0:
                raise IndexError
            asked = User.objects.get(id=id)
            return JsonResponse(asked.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only GET is allowed'
    })

@csrf_exempt
def update(request, id): # here we are passing raw json
    if request.method == 'PATCH':
        try:
            data = ast.literal_eval(request.body.decode("UTF-8"))['toPatch']
            topics = list(data.keys())
            if id is None or id == '':
                raise GenericError('NoIdToPatch') # should be an env var
            toUpdate = User.objects.get(id=id)
            for topic in topics:
                if topic not in allowed_to_update:
                    raise GenericError('ForbiddenUpdateof:{}'.format(topic)) # should be an env var
                toUpdate.__setattr__(topic, data[topic])
            toUpdate.save()
            return JsonResponse(toUpdate.toJson(), status=204)
        except GenericError as err:
            return JsonResponse(err.toJson(), status=403)
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=403)
    return JsonResponse({
        'code':405,
        'message': 'Only PATCH is allowed'
    })

@csrf_exempt
def delete(request, id=0):
    if request.method == 'DELETE':
        try:
            resp = User.objects.get(id=id).delete()
            if resp[0] == 1:
                return JsonResponse({
                    'code': 200,
                    'message': 'the user {} was deleted'.format(id)   # should just change the flag is_active to keep the data
                })
            raise IndexError
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only DELETE is allowed'
    })