from organizations.models import Organization
from users.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from .models import Project
from .errors import GenericError # where should be the generic error ? betterlife it seems
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json
import ast

allowed_to_update = ['title', 'description', 'members'] #TODO: should be an env var

def status():
    return HttpResponse('UP')

@csrf_exempt
def create(request): # add mandatory fields (name, ...) + here we are using form data
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            if 'organization' not in data:
                raise GenericError('AProjectCannotExistWithoutAnOrganization')
            organization = Organization.objects.get(id=data['organization'])
            owner = User.objects.get(id=data['owner'])
            if owner.role != 1 and owner.role != 2 and owner.role != 3:
                raise GenericError('ThisUserCannotBeOwner')
            new = Project(
                title = data['title'],
                description = data['description'],
                goal = data['goal'],
                owner = owner
            )
            new.save()
            if 'members' in data:
                tmp = None
                for id in data['members']:
                    tmp = User.objects.get(id=id)
                    if tmp.role == 5:
                        new.members.add(tmp)
            return JsonResponse(new.toJson())
        except GenericError as err:
            return JsonResponse(err.toJson(), status=400)
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only POST is allowed'
    })

def getAProject(request, id = 0): # through ID | id = 0, bad idea?
    if request.method == 'GET':
        try:
            if id == 0:
                raise IndexError
            asked = Project.objects.get(id=id)
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
            toUpdate = Project.objects.get(id=id)
            for topic in topics:
                if topic not in allowed_to_update:
                    raise GenericError('ForbiddenUpdateof{}'.format(topic)) # should be an env var
                if topic == 'members':
                    newUser = None
                    for id in data[topic]:
                        newUser = User.objects.get(id=id)
                        if newUser.role == 5:
                            toUpdate.members.add(newUser)
                        else:
                            raise PermissionDenied
                else:
                    toUpdate.__setattr__(topic, data[topic])
            toUpdate.save()
            return JsonResponse(toUpdate.toJson(), status=204)
        except GenericError as err:
            return JsonResponse(err.toJson(), status=403)
        except PermissionDenied as err:
            return JsonResponse({"message": 'you are tring to update the members with a user which have not the right role'}, status=403)
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
            resp = Project.objects.get(id=id).delete()
            return JsonResponse({
                'code': 200,
                'message': 'the project {} was deleted'.format(id)   # should just change the flag is_active to keep the data
            })
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only DELETE is allowed'
    })