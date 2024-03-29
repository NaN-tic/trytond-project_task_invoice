# This file is part of project_task_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        if 'required' in cls.project_invoice_method.states:
            del cls.project_invoice_method.states['required']
        if 'invisible' in cls.project_invoice_method.states:
            del cls.project_invoice_method.states['invisible']
        if 'invisible' in cls.party.states:
            del cls.party.states['invisible']

        if not 'required' in cls.party.states:
            cls.party.states['required'] = True
        if 'type' not in cls.party.depends:
            cls.party.depends.add('type')
        if 'parent' not in cls.party.depends:
            cls.party.depends.add('parent')
        if 'invisible' in cls.effort_duration.states:
            del cls.effort_duration.states['invisible']

        if hasattr(cls, 'invoice_standalone'):
            cls.invoice_standalone.states['invisible'] = (
                Eval('invoice_method') == 'manual')

        cls._buttons.update({
                'invoice': {
                    'invisible': (Eval('project_invoice_method', 'manual')
                            == 'manual'),
                    },
                })

    @fields.depends('_parent_parent.id', 'parent')
    def on_change_with_party(self, name=None):
        if self.parent and self.parent.party:
            return self.parent.party.id

    def on_change_with_invoice_method(self, name=None):
        res = super(Work, self).on_change_with_invoice_method(name)
        if self.project_invoice_method:
            return self.project_invoice_method
        return res
