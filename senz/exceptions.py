__author__ = 'wzf'

from senz.common.openstack.exceptions import *

class Invalid(NeutronException):
    pass

class NotEnouphData(Invalid):
    message = 'Not enouph %(param)s data for method '

class UpdateDataError(BadRequest):
    message = 'Update data error : %(msg)s'


if __name__ == '__main__':
    raise NotEnouphData(param = 'UserLocationTrace')