from odoo import models,fields,api
from odoo.exceptions import ValidationError

class FieldVisitLineEpt(models.Model):
    _name='field.visit.line.ept'
    _description='Field Visit Line Ept'

    # product_id - required - M2O
    # ● uom_id - required - M2O
    # ● qty - required - value must be greater than zero
    # ● field_visit_id - M2O - field.visit.ept
    product_id=fields.Many2one(comodel_name='product.ept',string='Product Id', required=True,help='Product id of the field visit line ept')
    uom_id=fields.Many2one(comodel_name='product.uom.ept',string='Uom Id', required=True,help='UOm id of the field visit line ept')
    qty= fields.Integer(string='Quantity', help='qutantity  of the field visit line ept', required=True)
    field_visit_id=fields.Many2one(comodel_name='field.visit.ept',string='Field Visit Id',help='field visit id of the field visit line ept')

    @api.constrains('qty')
    def check_commission(self):
        if (self.qty < 0):
            raise ValidationError('Warning ! Quantity  must me Greater than Zero')