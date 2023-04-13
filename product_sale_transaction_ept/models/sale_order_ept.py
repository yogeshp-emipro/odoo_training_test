from odoo import models, fields, api

class SaleOrderEpt(models.Model):
    _name = 'sale.order.ept'
    _description = 'Sale Order Ept'

    name = fields.Char(string='Name', default='New Order', help='name of the sale order ept')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Partner', help='Partner of the sale order ept')
    order_date = fields.Date(string='Order Date', help='Order Date of the sale order', default=fields.Date.today())
    order_line_ids = fields.One2many(comodel_name='sale.order.line.ept', inverse_name='sale_order_id',
                                     string='Order Line Ids', ondelete='cascade',
                                     help='order  line ids of sale order ept')
    order_total = fields.Float(string='Order Total', help='order total of the sale order ept',
                               compute='_compute_order_total')
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.sale.order.ept')
        return super(SaleOrderEpt, self).create(vals)

    @api.depends('order_line_ids')
    def _compute_order_total(self):
        for order in self:
            total = 0
            for orderline in order.order_line_ids:
                total += orderline.subtotal_without_tax
            order.order_total = total
