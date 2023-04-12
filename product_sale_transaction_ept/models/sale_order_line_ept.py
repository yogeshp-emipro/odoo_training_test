from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLineEpt(models.Model):
    _name = 'sale.order.line.ept'
    _description = 'Sale Order Line Ept'

    # product_id - product.ept -M2O - required
    # ● uom_id - product.uom.ept - M2O - required
    # ● unit_price - Float - 2 decimals - required - must be greater than zero
    # ● subtotal_without_tax - Float - 2 decimals - compute - store True - depends
    # on qty, unit price and product
    # ● produtct_qty - Float - 2 decimals - make sure qty is greater than zero
    product_id = fields.Many2one(comodel_name='product.ept', string='Product Id', required=True,
                                 help='Product id of the field sale order line ept')

    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='Uom Id', required=True,
                             help='Uom id of the field sale order line ept')
    unit_price = fields.Float(string='Unit Price', help='unit price of the sale order line ept')

    subtotal_without_tax = fields.Float(string='Order Total', help='order total of the sale order ept',
                                        compute='_compute_subtotal_without_tax', store=True)
    product_qty = fields.Float(string='FollowUp Days', help='FollowUp day  of the partner')

    sale_order_id=fields.Many2one(comodel_name='sale.order.ept', string='Sale Order Id',
                             help='sale order  id of the field sale order line ept')

    @api.constrains('followup_days')
    def check_commission(self):
        if (self.produtct_qty < 0):
            raise ValidationError('Warning ! Product qty must me Greater than Zero')

    @api.depends('product_id', 'unit_price', 'product_qty')
    def _compute_subtotal_without_tax(self):
        for orderline in self:
            orderline.subtotal_without_tax = 0
