# -*- coding: utf-8 -*-
{
    'name': "POC mails",

    'summary': """
        POC for emails""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Odoo SA",
    'website': "http://www.odoo.com",
    'sequence': 1,
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'mass_mailing',
    ],

    # always loaded
    'data': [
        'views/mailing_mailing.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
