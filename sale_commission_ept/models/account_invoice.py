from odoo import models,fields

class AccountInvoice(models.Model):
    _inherit='account.move'

    commission_id=fields.Many2one(comodel_name='sales.commission.ept',string='Commission',help='id of the commission ') 