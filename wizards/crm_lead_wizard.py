# -*- coding: utf-8 -*-

from odoo import models, fields, api
import io
import base64
import xlsxwriter


class CrmLeadWizard(models.TransientModel):
    _name = 'crm.lead.wizard'
    _description = 'Wizard para reintentar oportunidades de ventas perdidas'

    fecha_inicio = fields.Date(string='Fecha de inicio', required=True)
    fecha_fin = fields.Date(string='Fecha de fin', required=True)

    def action_print_excel_report(self):
        stage_id = int(self.env['ir.config_parameter'].sudo().get_param('crm.lost_stage_id', default=0))
        stage = self.env['crm.stage'].browse(stage_id)

        print("-------------------------------------")
        print(stage.name)
        print(stage_id)

        domain = [
            ('type', '=', 'opportunity'),
            # ('won_status', '=', 'lost'),
            ('stage_id', '=', stage_id),
            ('date_last_stage_update', '>=', self.fecha_inicio),
            ('date_last_stage_update', '<=', self.fecha_fin),
        ]
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
            'Nombre',
            'Cliente',
            'Vendedor',
            'Etapa',
            'Ingreso esperado',
            'Fecha creación',
        ]

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # 5. Datos
        row = 1
        for lead in oportunidades:
            worksheet.write(row, 0, lead.name or '')
            worksheet.write(row, 1, lead.partner_id.name or '')
            worksheet.write(row, 2, lead.user_id.name or '')
            worksheet.write(row, 3, lead.stage_id.name or '')
            worksheet.write(row, 4, lead.expected_revenue or 0)
            worksheet.write(row, 5, lead.create_date, date_format)
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