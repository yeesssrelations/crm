# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class Mail(models.Model):
    _inherit = 'mail.mail'

    body_html = fields.Text()

class TestMassMailing(models.TransientModel):
    _inherit = 'mailing.mailing.test'

    def send_mail_test(self):
        self.ensure_one()
        mails = self.env['mail.mail']
        mailing = self.mass_mailing_id
        test_emails = tools.email_split(self.email_to)
        mass_mail_layout = self.env.ref('mass_mailing.mass_mailing_mail_layout')
        for test_mail in test_emails:
            # Convert links in absolute URLs before the application of the shortener
            body = mailing.body_html
            # body = self.env['mail.thread']._replace_local_links(mailing.body_html)
            # body = tools.html_sanitize(body, sanitize_attributes=True, sanitize_style=True)
            mail_values = {
                'email_from': mailing.email_from,
                'reply_to': mailing.reply_to,
                'email_to': test_mail,
                'subject': mailing.subject,
                'body_html': body, # mass_mail_layout.render({'body': body}, engine='ir.qweb', minimal_qcontext=True),
                'notification': True,
                'mailing_id': mailing.id,
                'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
                'auto_delete': True,
                'mail_server_id': mailing.mail_server_id.id,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mails |= mail
        mails.send()
        return True