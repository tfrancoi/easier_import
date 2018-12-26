# -*- coding: utf-8 -*-
from odoo import models, api

class BaseModel(models.BaseModel):
    _inherit = 'base'
    
    @api.model
    def load(self, fields, data):
        if not self.env.context.get('defer_fields_computation'):
            return super(BaseModel, self).load(fields, data)

        with self.env.norecompute():
            res = super(BaseModel, self).load(fields, data)
        self.recompute()

        return res