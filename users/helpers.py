from users.errors import NoValueError
from .models import User
import string

def clean_string(data, key, forbidden):
    try:
        dirty = data[key]
    except Exception as err:
        raise NoValueError(key)
    if dirty is None or dirty == '':
        raise NoValueError(key)
    return dirty.translate(str.maketrans('', '', forbidden)) # should we clean the string or throw an error ???

def create_user_with_role(data, role=5):
    print(data)
    email = clean_string(data, 'email', string.punctuation.replace('@', '').replace('.', ''))
    username = clean_string(data, 'username', string.punctuation)
    first_name = clean_string(data, 'first_name', string.punctuation)
    last_name = clean_string(data, 'last_name', string.punctuation)
    password = clean_string(data, 'password', '') # front should send an hash
    new = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password, role=role)
    new.save()
    return new