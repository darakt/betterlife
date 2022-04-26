from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from users.models import User
from users.errors import GenericError, NoValueError
from django.db import IntegrityError
from django.http import JsonResponse
from users.helpers import clean_string
from django.contrib.auth.models import AbstractUser, Group, Permission
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
            email = clean_string(request.POST, 'email', string.punctuation.replace('@', '').replace('.', ''))
            username = clean_string(request.POST, 'username', string.punctuation)
            first_name = clean_string(request.POST, 'first_name', string.punctuation)
            last_name = clean_string(request.POST, 'last_name', string.punctuation)
            password = clean_string(request.POST, 'password', '') # front should send an hash
            new = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            new.save()
            return JsonResponse(new.toJson())
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Onyly POST is allowed'
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
        'message': 'Onyly GET is allowed'
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
            print(err)
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=403)
    return JsonResponse({
        'code':405,
        'message': 'Onyly PATCH is allowed'
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
        'message': 'Onyly DELETE is allowed'
    })