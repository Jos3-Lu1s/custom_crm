# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
       area_id = fields.Many2one("crm.area", string="Area", tracking=True)