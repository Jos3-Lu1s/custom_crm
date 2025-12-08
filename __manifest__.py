# -*- coding: utf-8 -*-
{
    'name': "Custom CRM",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Tekuno",
    'website': "https://tekuno.mx/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm','zhm_crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_kanban_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}

