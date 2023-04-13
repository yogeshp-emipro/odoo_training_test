from odoo import models, fields
from odoo import api
from odoo.exceptions import ValidationError


class ResPartnerEPT(models.Model):
    _name = "res.partner.ept"
    _description = " Res Partner  EPT"

    name = fields.Char(string='Partner Name', help='Name of the partner',required=True)
    next_visit_date = fields.Date(string='Next Visit Date', help=' Next Visit Date of the partner')
    followup_days = fields.Integer(string='FollowUp Days', help='FollowUp day  of the partner')
    field_visit_count=fields.Integer(string='Visit Count', help='Visit count day of the partner')
    field_visit_ids=fields.One2many(comodel_name='field.visit.ept',inverse_name='partner_id'  ,string='Field Visit Line Ids',
                                           help='field visit line ids of res partner ept')
    @api.constrains('followup_days')
    def check_commission(self):
        if (self.followup_days < 0):
            raise ValidationError('Warning ! FollowUp Days  must me Greater than Zero')
    def action_open_field_visit(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product_sale_transaction_ept.action_field_visit_ept')
        if len(self.field_visit_ids) > 1:
            action['domain'] = [('id', 'in', self.field_visit_ids.ids)]
        else:
            form_view = [(self.env.ref('product_sale_transaction_ept.view_field_visit_ept_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = self.field_visit_ids.id
        return action