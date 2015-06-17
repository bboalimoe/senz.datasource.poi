#-*- coding:utf-8 -*-
from SenzPoi.senz.common import config, settings

__author__ = 'wuzhifan'

import inspect
import logging

from senz.common import config, settings
from SenzPoi.senz.common.openstack import importutils
from senz.exceptions import *


LOG = logging.getLogger(__name__)

def get_current_function_name():
    return inspect.stack()[1][3]

def task(func):
    ''' indicate whether method is a task in controller

    '''
    def wrapper(self, context, *args, **kwargs):
        job = func.func_name
        pipeline = self.pipeline[job]
        pipeline.run(context)
        return func(self, context, *args, **kwargs)

    return wrapper


class Pipeline(object):
    def __init__(self, controller, job, task_list):
        self.controller = controller
        self.job = job
        self.managers = {}
        self.task_list = task_list
        for t in task_list:
            task = config.get_task(t)
            if not task:
                raise SenzExcption(msg="Can not find task %s in pipeline %s for controller %s" %
                                       (t, job, controller.__class__.__name__))

            manager_class = importutils.import_class(task['manager'])
            self.managers[t] = manager_class(self, task)

    def run(self, context):
        '''Run tasks of pipeline in order.

        :param context: request context
        :return:task results, success task list and failure task list
        '''
        LOG.debug("start task list %s" % self.task_list)

        context['results'] = {}

        for task in self.task_list:

            task_detail = config.get_task(task)

            method = getattr(self.managers[task], task_detail['method'], None)

            if not method:
                LOG.error('Request task method not implemented.')
                raise NotImplemented(function_name=task_detail['method'])


            arg_spec = inspect.getargspec(method)

            #print "arg spec %s " % str(arg_spec)

            arg_names = arg_spec.args
            arg_names.remove('self')

            arg_defaults = arg_spec.defaults
            if arg_defaults:
                #if context has default this will be wrong!
                no_default_args_len = len(arg_names) - len(arg_defaults)
            else:
                no_default_args_len = len(arg_names)

            kwargs = {}
            for i in range(len(arg_names)):
                if arg_names[i] == 'context' and not context.get('context'):
                    kwargs['context'] = context
                    continue

                arg = context.get(arg_names[i])
                if arg is not None:
                    kwargs[arg_names[i]] = arg
                elif i >= no_default_args_len:
                    #use default value if arg not in context
                    kwargs[arg_names[i]] = arg_defaults[i - no_default_args_len]

            if len(kwargs) != len(arg_names):
                LOG.info('Not enough args for task %s in pipeline of %s for %s job, workflow will'
                             'skip it.' % (task, self.controller.__class__.__name__, self.job))
                continue

            #LOG.debug("Get args %s in %s task." % (kwargs, task))
            res = method(**kwargs)

            if res:
                context['results'][task] = res

            if task_detail.get('store'):
                self.managers[task].store(context)


        return context['results']


class ControllerBase(object):
    def __init__(self):
        '''Init pipelines depend on jobs in settings of this controller

        '''
        self.pipeline = {}
        control_settings = settings.controllers[self.__class__.__name__]
        jobs = control_settings['jobs']
        for job in jobs:
            self.pipeline[job] = Pipeline(self, job, jobs[job])