from odoo import models,fields


class ProductUomEpt(models.Model):
    _name='product.uom.ept'
    _description='Product Uom Ept'

    name=fields.Char(string='Product Uom name',help='Product Uom ept')
