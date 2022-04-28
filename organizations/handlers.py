from users.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User, get_users_from_ids
from .models import Organization
from .errors import GenericError # where should be the generic error ? betterlife it seems
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json
import ast

allowed_to_update = ['name', 'description', 'admins', 'members'] #TODO: should be an env var

def status():
    return HttpResponse('UP')

@csrf_exempt
def create(request): # add mandatory fields (name, ...) + here we are using form data
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            created_by = User.objects.get(id=data['created_by'])
            admins = []
            if 'admins' in data: # could be a function, worth ?
                tmp = None
                for id in data['admins']:
                    tmp = User.objects.get(id=id)
                    if tmp.role == 1 or tmp.role == 2:
                        admins.append(tmp)
            admins.append(created_by)
            members = []
            if 'members' in data:
                tmp = None
                for id in data['members']:
                    tmp = User.objects.get(id=id)
                    if tmp.role == 3:
                        members.append(tmp)
            new = Organization(
                name = data['name'],
                description = data['description'],
                language = data['language']
            )
            new.save()
            for admin in admins:
                new.admins.add(admin)
            for member in members:
                new.members.add(member)
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

def getAnOrganization(request, id = 0): # through ID | id = 0, bad idea?
    if request.method == 'GET':
        try:
            if id == 0:
                raise IndexError
            asked = Organization.objects.get(id=id)
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
            toUpdate = Organization.objects.get(id=id)
            for topic in topics:
                if topic not in allowed_to_update:
                    raise GenericError('ForbiddenUpdateof{}'.format(topic)) # should be an env var
                if topic == 'admins':
                    newAdmin = None
                    for id in data[topic]:
                        newAdmin = User.objects.get(id=id)
                        if newAdmin.role == 1 or newAdmin.role == 2:
                            toUpdate.admins.add(newAdmin)
                        else:
                            raise GenericError('The user {} is not an admin'.format(newAdmin.id))
                elif topic == 'members':
                    newMember = None
                    for id in data[topic]:
                        newMember = User.objects.get(id=id)
                        if newMember.role == 3:
                            toUpdate.members.add(newMember)
                        else:
                            raise GenericError('The user {} is not a member'.format(newMember.id))
                else:
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
            resp = Organization.objects.get(id=id).delete()
            return JsonResponse({
                'code': 200,
                'message': 'the organization {} was deleted'.format(id)   # should just change the flag is_active to keep the data
            })
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only DELETE is allowed'
    })