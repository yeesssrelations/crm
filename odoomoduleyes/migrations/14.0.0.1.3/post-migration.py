# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    leads = env['crm.lead'].search([])

    if leads:
        env.add_to_compute(leads[0]._fields['cumul_pa'], leads)
        env.add_to_compute(leads[0]._fields['total_coupon'], leads)
        env.add_to_compute(leads[0]._fields['total_coupon_used'], leads)
