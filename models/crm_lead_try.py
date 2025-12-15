# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class CrmLeadTry(models.Model):
    _inherit = 'crm.lead'

    intentar_de_nuevo = fields.Boolean(
        string="Intentar de Nuevo",
        default=False,
        help="Indica si se debe intentar de nuevo con esta oportunidad."
    )

    def load(self, fields_list, data_list):
        fields_list = list(fields_list)
        for row in data_list:
            if "intentar_de_nuevo" in fields_list and "name" and "stage_id" in fields_list:
                id_try = fields_list.index("intentar_de_nuevo")
                id_name = fields_list.index("name")
                id_stage = fields_list.index("stage_id")
                deadline_date= fields_list.index("date_deadline")
                # IMPORTANTE: El valor puede venir 'True', '1', 'VERDADERO', etc
                valor_try = str(row[id_try]).strip().upper() if row[id_try] else ""
                valor_stage= str(row[id_stage]).strip()
                if row[id_name] and row[deadline_date] and valor_try in ("1", "TRUE", "VERDADERO", "YES", "SI") and valor_stage == "Perdido":
                    stage_perdido = self.env["crm.stage"].search([("name", "=", "Perdido")], limit=1)
                    stage_nuevo   = self.env["crm.stage"].search([("name", "=", "Nuevo")], limit=1)
                   
                    valor_deadline = row[deadline_date]
                    if valor_deadline:
                        valor_deadline = str(valor_deadline).strip()

                    if "-" in valor_deadline and len(valor_deadline) == 10:
                        pass

                    elif "/" in valor_deadline:
                        try:
                            d, m, y = valor_deadline.split("/")
                            row[deadline_date] = f"{y}-{m}-{d}"
                            _logger.warning(f">>>>>>>>>>>>>>>>FECHA ACEPTADAAAAAAAAAAAAAAAAAAAAAA<<<<<<<<<<<<<<<<<<<")
                        except Exception:
                            raise UserError(f"Fecha inválida: {valor_deadline}")
                    else:
                        raise UserError(f"Formato de fecha no soportado: {valor_deadline}")

                    if not stage_perdido or not stage_nuevo:
                        raise UserError("Etapas 'Perdido' o 'Nuevo' no existen en crm.stage")

                    lead = self.env['crm.lead'].search([
                        ("name", "=", row[id_name]),
                        ("stage_id", "=", stage_perdido.id)
                    ], limit=1)
                    if lead:
                        nuevo_lead = lead.copy({
                            "name": f"{lead.name}",
                            "stage_id": stage_nuevo.id,
                            "intentar_de_nuevo": False,
                            "active": False
                        })
                        _logger.warning(f">>>>>>>>>>>>>>>>EL ESTATUS DEL LEAD FUE: {nuevo_lead}<<<<<<<<<<<<<<<<<<<")
                    _logger.warning(f">>>>>>>>>>>>>>>>HOOOOOOOOOOOOOOOOOOOOLAAAAAAAAAAAAA<<<<<<<<<<<<<<<<<<<")
                    
                    row[id_stage] = stage_nuevo.name
        return super().load(fields_list, data_list)