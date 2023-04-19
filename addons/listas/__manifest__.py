# -*- coding: utf-8 -*-
{
    'name': "listas",

    'summary': """
        Módulo para la gestion Alcaldia de Valledupar""",

    'description': """
        Este modulo fue desarrollado con el fin de promocionar la capacidad
        de desarrollo en Odoo
    """,

    'author': "jorge Solórzano",
    'website': "jorgej.solorzano@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #'views/prueba.xml',
        'views/menusyacciones.xml',
        #'views/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
