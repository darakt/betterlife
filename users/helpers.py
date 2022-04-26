import string
import html
from users.errors import NoValueError

def clean_string(post, key, forbidden):
    if key is None or key == '':
        raise NoValueError('key')
    dirty = post.get(key)
    if dirty is None or dirty == '':
        raise NoValueError(key)
    return dirty.translate(str.maketrans('', '', forbidden)) # should we clean the string or throw an error ???
