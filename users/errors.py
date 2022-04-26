import traceback
import json

class Error(Exception):
    # Base class
    pass

class NoValueError(Error):
    def __init__(self, var, message = 'this variable is empty and should not be!', *args):
        self.var = var
        self.message = message
        self.args = args

    def __str__(self):
        return '{} : {}'.format(self.var, self.message)

class GenericError(Error): # that way we can manage the logs here !! + here we should decide what is send to front in the case of an error
    def __init__(self, name):
        self.name = name
        self.traceback = traceback.format_exc()

    def __str__(self):
        return '{} : {}'.format(self.name, self.traceback)

    def toJson(self):
        jsonified = {}
        for key in self.__dict__.keys():
            if self.__dict__[key] is not None and self.__dict__[key] != '':
                # print('[{}] = {}'.format(key, self.__dict__[key]))
                jsonified[key] = self.__dict__[key]
        return jsonified