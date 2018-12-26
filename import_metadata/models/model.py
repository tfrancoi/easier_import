# -*- coding: utf-8 -*-

from copy import copy
from odoo import models, api


class Base(models.AbstractModel):
    _inherit = 'base'

    _metadata_field = ['create_uid', 'create_date', 'write_uid', 'write_date']

    def _write_metada(self, vals):
        """
            generate the query and execute it to upgrade metadata value directly in SQL since it's the only way to update them.
        """
        if self.env.context.get('write_metadata') and self.env.uid == 2:
            sql = 'update %s set %%s where id in %s' % (self._table, tuple(self.ids) if len(self.ids) > 1 else '(%s)' % self.id)
            set_clause = []
            values = []
            for field in self._metadata_field:
                if field in vals:
                    set_clause.append("%s=%%s" % field)
                    values.append(vals[field] or None)
            if values and set_clause:
                sql = sql % ', '.join(set_clause)
                self.env.cr.execute(sql, tuple(values))

    @api.multi
    def write(self, vals):
        vals_copy = copy(vals)
        res = super(Base, self).write(vals)
        self._write_metada(vals_copy)
        return res

    @api.model
    def create(self, vals):
        vals_copy = copy(vals)
        res = super(Base, self).create(vals)
        res._write_metada(vals_copy)
        return res