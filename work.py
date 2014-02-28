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
        res = super(Work, self).get_invoice_method(name)
        if self.project_invoice_method:
            return self.project_invoice_method
        return res

    def _get_lines_to_invoice(self, test=None):
        "Return lines for work and children"
        lines = []
        if test is None:
            test = self._test_group_invoice()
        lines += getattr(self, '_get_lines_to_invoice_%s' %
            self.invoice_method)()

        for children in self.children:
            if children.type == 'project':
                if test != children._test_group_invoice():
                    continue
            lines += children._get_lines_to_invoice(test=test)
        return lines


