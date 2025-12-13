
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    crm_lost_stage_id = fields.Many2one(
        'crm.stage',
        string="Etapa de Oportunidad Perdida",
        config_parameter='crm.lost_stage_id'
    )