from odoo import models, fields


class FieldVisitEpt(models.Model):
    _name = 'field.visit.ept'
    _description = 'Field Visit Ept'

    # ● name - char - sequence - FV-000001 - default - ‘New Visit’ - required
    # ● user_id - res.users - M2O - Salesperson
    # ● partner_id - res.partner.ept - M2O
    # ● visit_date - Date - default - Today
    # ● field_visit_line_ids - O2M - field.visit.line.ept
    # state - selection - (Draft, Completed, Cancel) - required - default - Draft
    # ● visit_log - Text - when visit is completed, make sure there is value stored in
    # this field, it should not be empty
    name = fields.Char(string='New Visit', help='New Visit of the field visit ept', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='SalePerson', help='Sale person of the visit field')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Partner', help='Partner of the visit field')
    visit_date = fields.Date(string='Visit Date', help='Visit Date of the partner', default=fields.Date.today())

    field_visit_line_ids = fields.One2many(comodel_name='field.visit.line.ept', inverse_name='field_visit_id',
                                           string='Field Visit Line Ids', ondelete='cascade',
                                           help='field visit line ids of field visit ept')
    state = fields.Selection(string='Visit State', selection=[('draft', 'Draft'), ('completed', 'Completed'),
                                                              ('cancel', 'Cancel')], default='draft',
                             help='state of the field vist ept')

    visit_log = fields.Text(string='Visit Log', help='visit log of  the field visit ept')
