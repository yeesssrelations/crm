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
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': [
        'mass_mailing',
        'marketing_automation',
    ],

    # always loaded
    'data': [
        'datas/functions.xml',
        'views/mailing_mailing.xml',
        'views/mail_mail.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
