from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.char(string='Customer Code', help='code of the partner')
