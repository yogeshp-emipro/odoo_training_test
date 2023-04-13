from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FieldVisitLineEpt(models.Model):
    _name = 'field.visit.line.ept'
    _description = 'Field Visit Line Ept'

    product_id = fields.Many2one(comodel_name='product.ept', string='Product Id', required=True,
                                 help='Product id of the field visit line ept')
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='Uom Id', required=True,
                             help='UOm id of the field visit line ept')
    unit_price = fields.Float(string='Unit Price', help='unit price  of the field visit line ept', required=True)
    qty = fields.Integer(string='Quantity', help='qutantity  of the field visit line ept', required=True)
    field_visit_id = fields.Many2one(comodel_name='field.visit.ept', string='Field Visit Id',
                                     help='field visit id of the field visit line ept')
    @api.constrains('qty')
    def check_commission(self):
        for filedline in self:
            if (filedline.qty < 0):
                raise ValidationError('Warning ! Quantity  must me Greater than Zero')
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.unit_price = self.product_id.price
            self.qty = 1
            self.uom_id = self.product_id.uom_id.id
