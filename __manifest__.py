# -*- coding: utf-8 -*-
{
    'name': "Custom CRM",

    'summary': "Personalizaciones en formularios y kanban de CRM Leads",

    'description': """
    
Este módulo realiza las siguientes personalizaciones en los **Leads de CRM**:

- Añade los campos **Comisión** y **Comisión Anual** en la vista kanban.
- Oculta el campo *Probabilidad* y varios elementos de la interfaz en el formulario de leads.

    """,

    'author': "Tekuno",
    'website': "https://tekuno.mx/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','zhm_crm','contacts'],

    # always loaded

    "data": [
        "security/ir.model.access.csv",
        "views/crm_buttons_inherit_views.xml",
        "views/crm_lead_form_inherit.xml",
        "views/crm_lead_kanban_inherit.xml",
        "views/crm_lead_tree_inherit.xml",
        'views/crm_search_lead_inherit.xml',
        'views/res_partner_form_inherit.xml',
        "views/res_config_settings_views.xml",
        "wizards/crm_lead_wizard.xml"
    ],

    'assets':{
        'web.assets_backend':[
            'custom_crm/static/src/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
}

