# -*- coding: utf-8 -*-

from itertools import groupby
from odoo import models, fields, api
from _collections import defaultdict

def _extract_xml_id(xml_id):
    id_splitted = xml_id.split('.')
    if len(id_splitted) == 1:
        return '', id_splitted[0]

    return id_splitted[0], '.'.join(id_splitted[1:])

class ResIdMixin(models.AbstractModel):
    """

    """
    _name = "import.res_id.mixin"

    _model_field = 'res_model'
    _res_id_field = 'res_id'

    res_external_id = fields.Char(compute="_get_external_id",
                                  inverse="_set_external_id",
                                  string="Related object external id")



    @api.multi
    def _get_external_id(self):
        rec_per_model_res_id = defaultdict(list)
        for rec in self:
            rec_per_model_res_id[(rec[self._model_field], rec[self._res_id_field])].append(rec)

        domain = []
        for model, group in groupby(self, lambda x: x[self._model_field]):
            domain.extend(['&', ('model', '=', model), ('res_id', 'in', [g[self._res_id_field] for g in group])])
        domain = ['|'] * (len(domain) / 3 -1) + domain

        for external_id in self.env['ir.model.data'].search(domain):
            for record in rec_per_model_res_id[(external_id.model, external_id.res_id)]:
                record.res_external_id = "%s.%s" % (external_id.module, external_id.name)

    @api.multi
    def _set_external_id(self):
        xml_ids = [_extract_xml_id(rec.res_external_id) for rec in self if rec.res_external_id]
        if not xml_ids:
            return
        rec_per_xml_id = defaultdict(list)
        for rec in self.filtered('res_external_id'):
            rec_per_xml_id[_extract_xml_id(rec.res_external_id)].append(rec)

        domain = []
        for module, group in groupby(xml_ids, lambda x: x[0]):
            domain.extend(['&', ('module', '=', module), ('name', 'in', [g[1] for g in group])])
        domain = ['|'] * int(len(domain) / 3 -1) + domain
        for external_id in self.env['ir.model.data'].search(domain):
            for record in rec_per_xml_id[(external_id.module, external_id.name)]:
                record[self._model_field] = external_id.model
                record[self._res_id_field] = external_id.res_id

class IrAttachment(models.Model):
    _name = "ir.attachment"
    _inherit = ["ir.attachment", "import.res_id.mixin"]


class MailMessage(models.Model):
    _name = 'mail.message'
    _inherit = ['mail.message', 'import.res_id.mixin']

    _model_field = 'model'
    _res_id_field = 'res_id'

class MailFollowers(models.Model):
    _name = 'mail.followers'
    _inherit = ['mail.followers', "import.res_id.mixin"]
