from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_partner_code = fields.Char(string='Customer Own code')
