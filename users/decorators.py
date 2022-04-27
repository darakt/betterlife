from .models import User
import json
# Cons : one more access
# Pro: clean
def need_to_be_superuser_one_arg(f):
    def inner(request):
        data = json.loads(request.body.decode("UTF-8"))
        askedBy = User.objects.get(id=data['askedBy'])
        return f(request)
    return inner
