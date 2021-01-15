from odoo import models, api


class SetValuesNethys(models.AbstractModel):
    _name = 'set.values'
    _description = 'Set values'

    @api.model
    def _delete_template(self):
        mass_mail_layout = self.env.ref('mass_mailing.mass_mailing_mail_layout', raise_if_not_found=False)
        if mass_mail_layout:
            mass_mail_layout.unlink()
