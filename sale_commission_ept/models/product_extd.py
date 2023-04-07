from odoo import models, fields

class ProductExt(models.Model):
    _inherit = 'product.product'

    product_ept_id = fields.Many2one(comodel_name='product.product', string='Product',
                                         help='id of the product',domain=[('detailed_type','=','service')])
