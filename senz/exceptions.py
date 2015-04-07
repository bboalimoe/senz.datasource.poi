__author__ = 'wzf'

import sys

def error_info():
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return info

class SenzExcption(Exception):
    code = 500
    message = 'Senz handle error: %(msg)s'

class NotImplemented(SenzExcption):
    code = 501
    message = 'Function %(funtionName) not implemented.'

class BadRequest(SenzExcption):
    code = 400
    message = 'Bad %(resource)s request: %(msg)s'


class NotFound(SenzExcption):
    code = 404
    message = 'Not found resouces: %(msg)s'


class Conflict(SenzExcption):
    pass


class NotAuthorized(SenzExcption):
    message = "Not authorized."


class ServiceUnavailable(SenzExcption):
    message = "The service is unavailable"


class InUse(SenzExcption):
    message = "The resource is inuse"


class DuplicatedExtension(SenzExcption):
    message = "Found duplicate extension: %(alias)s"


class Invalid(SenzExcption):
    pass


class NotEnouphData(Invalid):
    message = 'Not enouph %(param)s data for method '


class DataCRUDError(BadRequest):
    message = 'Handle data CRUD method error : %(msg)s'



if __name__ == '__main__':
    raise NotEnouphData(param = 'UserLocationTrace')