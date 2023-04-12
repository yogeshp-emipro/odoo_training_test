from odoo import models, fields


class SaleOrderEpt(models.Model):
    _name = 'sale.order.ept'
    _description = 'Sale Order Ept'

    #  name - char - required - default - ‘New’ - generate the sequence - SO-00001
    # ● partner_id - res.partner.ept - M2O - required
    # ● order_date - Date - required
    # ● order_line_ids - sale.order.line.ept - O2M
    # ● order_total - Float - 2 decimals - computed - store True - depends on
    # subtotal_without_tax of order_line_ids

    name = fields.Char(string='Name', help='name of the sale order ept')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Partner', help='Partner of the sale order ept')
    order_date = fields.Date(string='Order Date', help='Order Date of the sale order', default=fields.Date.today())
    order_line_ids = fields.One2many(comodel_name='sale.order.line.ept', inverse_name='sale_order_id',
                                     string='Order Line Ids', ondelete='cascade',
                                     help='order  line ids of sale order ept')

    order_total = fields.Float(string='Order Total', help='order total of the sale order ept',
                               compute='_compute_order_total')

    def _compute_order_total(self):
        for order in self:
            order.order_total = 0
