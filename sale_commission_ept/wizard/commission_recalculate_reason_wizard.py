from odoo import models,fields

class CommissionRecalculateReasonWizard(models.TransientModel):

    _name='commission.recalculate.reason.wizard'
    _description='Commission Recalculate Reason Wizard'

    name=fields.Text(string='Reason',required=True)
    sales_commission_id=fields.Many2one(comodel_name='sales.commission.ept',string='Sales Commission Id')
#     name - Text - required - Label - Reason
#     sales_commission_id - M2O - sales.commission.ept - readonly
#     Value should be automatically fill the current commission record in it, when the wizard is opened


    def recalculate_commission(self):

        pass