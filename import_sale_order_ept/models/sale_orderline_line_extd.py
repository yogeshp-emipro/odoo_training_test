from odoo import fields,models

class SaleOrderlinekExtd(models.Model):

    _inherit="sale.order.line"

    cost_price=fields.Float(string='Cost Price')







































































































































































































































































