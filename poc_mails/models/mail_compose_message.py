# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    body = fields.Text(sanitize_style=False)
