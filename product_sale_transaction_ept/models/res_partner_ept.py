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

    @api.constrains('followup_days')
    def check_commission(self):
        if (self.followup_days < 0):
            raise ValidationError('Warning ! FollowUp Days  must me Greater than Zero')

    # name - char - required
    # ● next_visit_date - Date
    # ● followup_days - integer - must be greater than zero, otherwise don’t allow to
    # create or update the data
    # ● field_visit_count - integer - It should show the total count of field.visit.ept
    # for this customer. Add a button box when clicked on it, should show the list
    # view field.visit.ept for this customer and also form view should be able to
    # open from it.