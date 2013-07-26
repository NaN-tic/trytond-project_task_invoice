#This file is part of project_task_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import PoolMeta, Pool

__metaclass__ = PoolMeta

__all__ = ['Work']


class Work:
    __name__ = 'project.work'

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        if 'required' in cls.project_invoice_method.states:
            del cls.project_invoice_method.states['required']
        if 'invisible' in cls.project_invoice_method.states:
            del cls.project_invoice_method.states['invisible']

    def get_invoice_method(self, name):
        if self.type == 'project':
            return self.project_invoice_method
        elif self.project_invoice_method:
            return self.project_invoice_method
        elif self.parent:
            return self.parent.invoice_method
        else:
            return 'manual'
