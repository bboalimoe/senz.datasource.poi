#-*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import inspect
import logging
from senz.common import config, settings
from senz.common.openstack import importutils

LOG = logging.getLogger(__name__)

def get_current_function_name():
    return inspect.stack()[1][3]

class Pipeline(object):
    def __init__(self, controller, job, task_list):
        self.controller = controller
        self.job = job
        self.managers = {}
        self.task_list = task_list
        for t in task_list:
            task = config.get_task(t)
            manager_class = importutils.import_class(task['manager'])
            self.managers[t] = manager_class(self, t)

    def run(self, context):
        #todo : handle method with optional args !!!!!!
        '''Run tasks of pipeline in order.

        :param context: request context
        :return:task results, success task list and unsuccess task list
        '''
        context['results'] = {}

        for task in self.task_list:
            task_detail = config.get_task(task)
            arg_names = task_detail['args']
            kwargs = {}
            for name in arg_names:
                arg = context.get(name)
                if arg:
                    kwargs[name] = arg

            if len(kwargs) != len(arg_names):
                LOG.info('Not enough args for task %s in pipeline of %s for %s job, workflow will'
                             'skip it.' % (task, self.controller, self.job))
                continue

            method = getattr(self.managers[task], task)
            res = method(context, **kwargs)
            if res:
                context['results'][task] = res
            if task.get('store'):
                self.managers[task].store(context)

        return context['results']


class ControllerBase(object):
    def __init__(self):
        self.pipeline = {}
        control_settings = settings.controllers[self.__class__.__name__]
        jobs = control_settings['jobs']
        for job in jobs:
            self.pipeline[job] = Pipeline(self, job, jobs[job])