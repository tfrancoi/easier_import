# -*- coding: utf-8 -*-
from odoo import models, api

class BaseModel(models.BaseModel):
    _inherit = 'base'
    
    @api.model
    def load(self, fields, data):
        if self.env.context.get('defer_fields_computation'):
            with self.env.norecompute():
                res = super(BaseModel, self).load(fields, data)
            recs = self.search([('id', 'in', res['ids'])])
            recs.recompute()
        else:
            res = super(BaseModel, self).load(fields, data)
        return res
