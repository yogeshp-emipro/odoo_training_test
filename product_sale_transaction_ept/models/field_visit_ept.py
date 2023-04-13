from odoo import models, fields, api

import  datetime

class FieldVisitEpt(models.Model):
    _name = 'field.visit.ept'
    _description = 'Field Visit Ept'

    name = fields.Char(string='Name', default='New Visit', help='New Visit of the field visit ept', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='SalePerson', help='Sale person of the visit field',default=lambda self: self.env.user)
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Partner', help='Partner of the visit field')
    visit_date = fields.Date(string='Visit Date', help='Visit Date of the partner', default=fields.Date.today())

    field_visit_line_ids = fields.One2many(comodel_name='field.visit.line.ept', inverse_name='field_visit_id',
                                           string='Field Visit Line Ids',ondelete='cascade',
                                           help='field visit line ids of field visit ept')
    state = fields.Selection(string='Visit State', selection=[('draft', 'Draft'), ('completed', 'Completed'),
                                                              ('cancel', 'Cancel')], default='draft',
                             help='state of the field vist ept')

    visit_log = fields.Text(string='Visit Log', help='visit log of  the field visit ept')
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.field.visit.ept')
        return super(FieldVisitEpt,self).create(vals)
    def complete_visit(self):
        self.state='completed'
        partner = self.partner_id
        new_date = self.visit_date + datetime.timedelta(days=partner.followup_days)
        partner.write({'next_visit_date':new_date,'field_visit_count':partner.field_visit_count+1})
        self.visit_log='Hello %s Visit is completed '%(self.user_id.name)