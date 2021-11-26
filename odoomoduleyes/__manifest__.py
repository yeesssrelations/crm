# -*- coding: utf-8 -*-
{
    'name': "odoomoduleyes",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Yeesss",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.1.3',

    # any module necessary for this one to work correctly
    'depends': ['base','crm',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/personne.xml',
        'views/references.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
