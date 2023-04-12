from odoo import models,fields,api
from odoo.exceptions import ValidationError
class ProductEpt(models.Model):
    _name = 'product.ept'
    _description = 'Product Ept'

    name = fields.Char(string='Product Name', help='Name of the Product ept',required=True)
    price=fields.Float(string='Product Price', help='Price of the Product ept',required=True)
    sku=fields.Char(string='Product Sku', help='sku of the Product ept',required=True)
    uom_id=fields.Many2one(comodel_name='product.uom.ept', string='Product Uom Id', help='Id of the product uom ept',required=True)

    @api.constrains('commission_percentage', 'total_commission')
    def check_commission(self):
        if (self.price<0):
            raise ValidationError('Warning ! Price must me Greater than Zero')
