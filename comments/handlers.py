from turtle import title
from .models import Comment
from users.models import User

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from .errors import GenericError # where should be the generic error ? betterlife it seems
from django.http import JsonResponse
import json
import ast

allowed_to_update = ['text', 'title'] #TODO: should be an env var

def status():
    return HttpResponse('UP')

@csrf_exempt
def create(request): # add mandatory fields (name, ...) + here we are using form data
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
            creator = User.objects.get(id=data['written_by'])
            print(hasattr(data, 'in_response_to'))
            print(data['in_response_to'])
            if 'in_response_to' in data:
                print('it worked')
                try: # EAFP
                    in_response_to = Comment.objects.get(id=data['in_response_to'])
                except Exception as err:
                    raise GenericError('{}WithInResponseTo'.format(err.__class__.__name__))
            else:
                in_response_to = None
            if hasattr(data, 'in_response_to'):
                in_response_to = data['in_response_to']
            new = Comment(
                title=data['title'],
                text=data['text'],
                written_by=creator,
                in_response_to=in_response_to
            )
            new.save()
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

def getAComment(request, id = 0): # through ID | id = 0, bad idea? + get a comment without nested user or nested comment depends on the needs
    if request.method == 'GET':
        try:
            if id == 0:
                raise IndexError
            asked = Comment.objects.get(id=id)
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
            toUpdate = Comment.objects.get(id=id)
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
            resp = Comment.objects.get(id=id).delete()
            if resp[0] == 1:
                return JsonResponse({
                    'code': 200,
                    'message': 'the comment {} was deleted'.format(id)   # should just change the flag is_active to keep the data
                })
            raise IndexError
        except Exception as err:
            customError = GenericError(err.__class__.__name__)
            return JsonResponse(customError.toJson(), status=400)
    return JsonResponse({
        'code':405,
        'message': 'Only DELETE is allowed'
    })