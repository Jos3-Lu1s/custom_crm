
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    crm_lost_stage_id = fields.Many2one(
        'crm.stage',
        string="Etapa de oportunidad perdida",
        config_parameter='crm.lost_stage_id'
    )
    
    crm_retry_stage_id = fields.Many2one(
        'crm.stage',
        string="Etapa de reinicio de oportunidades",
        config_parameter='crm.retry_stage_id'
    )