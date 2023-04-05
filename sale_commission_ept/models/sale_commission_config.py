from odoo import models, fields, api


class SaleCommissionEpt(models.Model):
    _name = 'sale.commission.config'
    _description = 'Sale Commission Ept'

    name = fields.Char(string='Commission Name', help=' Name of the Sale commission ept ', required=True)
    commission_calculation_type = fields.Selection(string='Commission Calculation Type',
                                                   selection=[('confirmed orders', 'Confirmed Orders'),
                                                              ('confirmed invoices', 'Confirmed Invoices'),
                                                              ('paid invoices', 'Paid Invoices')],help='commission calculation type of the sale commission')
    commission_calculate_for=fields.Selection(string='Commission Calculate For',selection=[('sale person', 'Sale Person'),
                                                              ('sales team', 'Sales Team')],default='sale person',required=True,help='commission calculate for sale commission')

    commission_percentage=fields.Float(string='Commission Percentage',help='commission percentage of the sale commission')

    sale_manager_commission_based_on=fields.Selection(string='Sale Manager Commission ',selection=[('individual sales', 'Individual Sales'),
                                                              ('include team', 'Include Team'),('members also','Members Also')],required=True)

