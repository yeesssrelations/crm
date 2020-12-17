# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    body_html = fields.Text()
