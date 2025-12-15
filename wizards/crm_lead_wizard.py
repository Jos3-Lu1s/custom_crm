# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import io
import base64
import xlsxwriter
from io import BytesIO
from openpyxl import load_workbook
from odoo.exceptions import UserError


class CrmLeadWizard(models.TransientModel):
    _name = 'crm.lead.wizard'
    _description = 'Wizard para reintentar oportunidades de ventas perdidas'

    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')

    modo_operacion = fields.Selection([
        ('exportar', 'Exportar'),
        ('importar', 'Importar')
    ], string="Modo", default='exportar')

    archivo = fields.Binary(string="Subir archivo")

    def action_generar(self):
        if self.modo_operacion == 'exportar':
            stage_id = int(self.env['ir.config_parameter'].sudo().get_param('crm.lost_stage_id', default=0))
            stage = self.env['crm.stage'].browse(stage_id)

            domain = [
                ('type', '=', 'opportunity'),
                ('stage_id', '=', stage_id),
                ('date_last_stage_update', '>=', self.fecha_inicio),
                ('date_last_stage_update', '<=', self.fecha_fin),
            ]
            
            return self.crear_excel(domain)
        
        elif self.modo_operacion == 'importar':
            catalogo = self.leer_excel()
            print(catalogo)
            ids_a_perder = catalogo.get('no', [])
            ids_a_reintentar = catalogo.get('si', [])
            self.marcar_perdidas(ids_a_perder)
            self.duplicar_leads(ids_a_reintentar)
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def crear_excel(self, domain):
        oportunidades = self.env['crm.lead'].search(domain)

        # 2. Crear Excel en memoria
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Oportunidades')

        # 3. Formatos
        header_format = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

        # 4. Encabezados
        headers = [
            'Id',
            'Nombre',
            'Prima',
            'Cliente',
            'Vendedor',
            'Area',
            'Etapa',
            'Fecha creación',
            'Intentar de nuevo',
            'nuevo vencimiento',
        ]

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # 5. Datos
        row = 1
        for lead in oportunidades:
            worksheet.write(row, 0, lead.id or '')
            worksheet.write(row, 1, lead.name or '')
            worksheet.write(row, 2, lead.expected_revenue or 0)
            worksheet.write(row, 3, lead.partner_id.name or '')
            worksheet.write(row, 4, lead.user_id.name or '')
            worksheet.write(row, 5, lead.area_id.name or '')
            worksheet.write(row, 6, lead.stage_id.name or '')
            worksheet.write(row, 7, lead.create_date, date_format)
            worksheet.write(row, 8, 'No')
            worksheet.write(row, 9, '')
            row += 1

        workbook.close()
        output.seek(0)

        # 6. Crear adjunto
        attachment = self.env['ir.attachment'].create({
            'name': 'oportunidades.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        # 7. Descargar
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

        
    def leer_excel(self):
        if not self.archivo:
            raise UserError("Debes subir un archivo Excel")

        data = base64.b64decode(self.archivo)
        wb = load_workbook(filename=BytesIO(data), read_only=True)
        ws = wb.active

        headers = [cell.value for cell in next(ws.iter_rows(max_row=1))]

        if 'Id' not in headers:
            raise UserError("El archivo no contiene la columna 'Id'")
        if 'Intentar de nuevo' not in headers:
            raise UserError("Falta la columna 'Intentar de nuevo'")

        id_index = headers.index('Id')
        intentar_index = headers.index('Intentar de nuevo')

        catalogo = {
            'si': [],
            'no': []
        }

        for row in ws.iter_rows(min_row=2):
            record_id = row[id_index].value
            intentar = row[intentar_index].value

            if not record_id:
                continue

            valor = str(intentar).strip().lower() if intentar else 'no'

            if valor == 'si':
                catalogo['si'].append(record_id)
            else:
                catalogo['no'].append(record_id)

        return catalogo

    def marcar_perdidas(self, ids_a_perder):
        if ids_a_perder:
            oportunidades = self.env['crm.lead'].browse(ids_a_perder)
    
        # Solo marcar como perdido las que no estén ya perdidas o cerradas
        for opp in oportunidades:
            if opp.stage_id and not opp.probability == 0 and not opp.active == False:
                opp.action_set_lost()

    def duplicar_leads(self, ids):
        """
        Duplicar oportunidades según sus IDs y colocarlas en la primera etapa del equipo correspondiente.
        """
        if not ids:
            return self.env['crm.lead']

        oportunidades = self.env['crm.lead'].browse(ids)
        new_leads = self.env['crm.lead']

        for lead in oportunidades:
            new_lead = lead.copy(default={'stage_id': 1})
            new_leads += new_lead

        return new_leads