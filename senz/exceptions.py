__author__ = 'wzf'

from senz.common.openstack.exceptions import *

class Invalid(NeutronException):
    pass

class NotEnouphData(Invalid):
    message = 'Not enouph %(param)s data for method '

class DataCRUDError(BadRequest):
    code = 500
    message = 'Handle data CRUD method error : %(msg)s'


if __name__ == '__main__':
    raise NotEnouphData(param = 'UserLocationTrace')