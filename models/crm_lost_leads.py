from odoo import models, fields, api 

class CrmLostLeads(models.Model): 
    _inherit = 'crm.lead'
    retry_attempt = fields.Selection( 
        [('si','Sí'),('no','No')],
        string ='Intentar de nuevo',
        tracking = True,
        default = 'no'
    )
