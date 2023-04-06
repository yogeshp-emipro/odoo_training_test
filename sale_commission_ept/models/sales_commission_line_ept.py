from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SalesCommissionLineEpt(models.Model):
    _name = 'sales.commission.line.ept'
    _descripiton = 'Sales Commission Line Ept'
# transaction_date (date of related document, like sales order or invoice date)
# user_id - M2O - res.users - salesperson of sales order or invoice
# partner_id - M2O - res.partner - partner of either sales order or invoice
# source_document - Char - required
# name of either sales order or customer invoices based on the configuration in sales commission configuration
# amount - Float - 2 decimals - required
# It can be order total or invoice total without tax
# to_be_paid_commission_amount - Float - 2 decimals - compute - store True
# It will be the amount after applying the commission percentage to ‘amount’ field
# sale_commission_id - M2O - sales.commission.ept - required
    transaction_date=fields.Datetime(string='Transaction Date',help='transaction date of the sales commission line ept.')#related
    user_id = fields.Many2one(comodel_name='res.users', string='User', help='User  of the Sale Commission ')
    partner_id=fields.Many2one(comodel_name='res.partner', string='Partner', help='Partner  of the Sale Commission ')
    source_document=fields.Char(string='Name',help='Name of the sales commission line ept')#related
    amount=fields.Float(string='Commission Amount',help='amount of the sales commission line ept')
    to_be_paid_commission_amount=fields.Float(string='Commission Amount to Pay',compute='_compute_commission_amount_paid',help='amount of the commission to be paid for sales commission line ept')
    sale_commission_id=fields.Many2one(comodel_name='sales.commission.ept',string='Sale Commission Id',required=True,help='Id of the sale commission config')
    
    @api.depends('sale_commission_id')
    def _compute_commission_amount_paid(self):
        for commission in self:
            commission.to_be_paid_commission_amount=commission.amount*commission.sale_commission_id.commission_percentage/100




