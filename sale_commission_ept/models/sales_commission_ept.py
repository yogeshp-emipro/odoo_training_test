from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError
from lxml import etree
import json
import simplejson


class SalesCommissionEpt(models.Model):
    _name = 'sales.commission.ept'
    _descripiton = 'Sales Commission Ept'

    # name - Char - required
    # Example - March - April - 2023 Commission
    # sales_commission_config_id - M2O - sale.commission.config - required
    # Based on the configuration, sales calculation will be calculated
    # commission_calculate_for - selection[Salesperson, Sales Team] - compute - store - False - readonly - Label - Calculate Commission For
    # user_id - M2O - res.users
    # It can either be the salesperson or a sales manager
    # This field will be only visible if the commission_calculate_for is set as ‘Salesperson’, otherwise not
    # It will be only required, if commission_calculate_for is set as ‘Salesperson’ else not
    # team_id - M2O - crm.team
    # This field will only be visible if the commission_calculate_for is set as ‘Sales Team’, otherwise not
    # It will be only required, if commission_calculate_for is set as ‘Sales Team’ else not
    # from_date - Date - required
    # to_date - Date - required
    # Must be greater than the from_date at least 2 weeks
    # commission_percentage - Float - 2 decimals
    # This field value will be derived from the sales_config_id -> commission_percentage
    # This is regular field not related field and can be edited by user

    name = fields.Char(string='Commission name', help='Name of the sale commission ')
    sale_commission_config_id = fields.Many2one(comodel_name='sale.commission.config', string='Commission Config Id',
                                                required=True, help='Id of the sale commission config')
    commission_calculate_for = fields.Selection(string='Commission Calculate For',
                                                selection=[('sale person', 'Sale Person'),
                                                           ('sales team', 'Sales Team')],
                                                help='commission calculate for sale commission')
    user_id = fields.Many2one(comodel_name='res.users', string='User', help='User  of the Sale Commission ')
    team_id = fields.Many2one(comodel_name='crm.team', string='Team', help='Team  of the Sale Commission ')
    from_date = fields.Datetime(string='Commission From Date', required=True, default=fields.Datetime.now,
                                help="from date of the sale commission.")
    to_date = fields.Datetime(string='Commission To Date', required=True, help="to date of the sale commission.")

    commission_percentage = fields.Float(string='Commission Percentage',
                                         help='commission percentage of the sale commission')

    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('approved', 'Approved'),
                                        ('in-payment', 'In-Payment'), ('paid', 'Paid'),
                                        ('cancelled', 'Cancelled')], required=True,
                             help='state of the sale commission', default='draft')  # non clickable
    commission_lines_ids = fields.One2many(comodel_name='sales.commission.line.ept', inverse_name='sale_commission_id',
                                           string='Sale Commission Line ',
                                           help='sale commission line of sale commission ept')
    # sale_order_id=fields.Many2one(comodel_name='sale.order',string='Sale Order',help='sale order id of the sale commission ept')

    # commission_lines_ids - O2M - sales.commission.line.ept - inverse name -  sale_commission_id
    # In-line tree view
    # total_commission - Float - 2 decimals - compute - store True
    # Must be non-negative
    # Based on the value of ‘to_be_paid_commission_amount’ in sales commission lines
    # amount_residual - Float - 2 decimals - compute - store False
    # This will be calculated based on the invoice(purchase/vendor bill) generated for commission and the amount paid amount of that invoice
    # Need to show how much amount is still remaining to be paid by deducting whatever is paid amount in the invoice
    # commission_final_paid_date - Date - readonly
    # This will be set from the invoice, when the payments are made need to check if the invoice(bill) if fully paid, that date should be set in this field
    # Make sure partial payment dates are not allowed
    total_commission = fields.Float(string=' Total Commission',
                                    help=' total commission of the sale commission')
    amount_residual = fields.Float(string=' Amount Remaining',
                                   help='amount remaining of the sale commission')
    commission_final_paid_date = fields.Datetime(string='Commission Paid Date', readonly=True,
                                                 help="paid date of the sale commission.")

    @api.constrains('commission_percentage', 'total_commission')
    def check_commission(self):
        if (self.commission_percentage and self.commission_percentage < 1 or self.commission_percentage > 100) or (
                self.total_commission and self.total_commission < 1):
            raise ValidationError('Warning ! Commission Percentage cannot be negative and in range of 100')

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     context = self._context
    #     res = super(SalesCommissionEpt, self).fields_view_get(view_id=None, view_type='form', toolbar=False, submenu=False)
    # #
    #     if context.get('turn_view_readonly'):
    #         doc = etree.XML(res['arch'])
    #         if view_type == 'form':
    #             for node in doc.xpath("//field"):
    #                 node.set("readonly", '1')
    #                 node_values = node.get('modifiers')
    #                 modifiers = json.Loads(node_values)
    #                 modifiers["readonly"] = True
    #                 node.set("modifiers", simplejson.dumps())
    #             res['arch'] = etree.tostring(doc)
    #     return res

    @api.onchange('sale_commission_config_id')
    def onchange_sale_commission_config(self):
        self.commission_percentage = self.sale_commission_config_id.commission_percentage
        self.commission_calculate_for = self.sale_commission_config_id.commission_calculate_for

    def calculate_commission_line(self):
        commission_lines = []
        if self.sale_commission_config_id.commission_calculation_type == 'confirmed orders':
            if self.commission_calculate_for == 'sale person':
                sale_orders = self.env['sale.order'].search([('user_id', '=', self.user_id.id)])
            else:
                if self.sale_commission_config_id.sale_manager_commission_based_on == 'individual sales':
                    sale_orders = self.env['sale.order'].search([('user_id', '=', self.team_id.alias_user_id.id)])

                else:
                    sale_orders = self.env['sale.order'].search([('user_id', 'in', self.team_id.member_ids.ids)])

            for order in sale_orders:
                        commission_lines.append(Command.create({'transaction_date': order.date_order,
                                                                'user_id': order.user_id.id,
                                                                'partner_id': order.partner_id.id,
                                                                'source_document': order.partner_id.name,
                                                                'amount': order.amount_total}))
            self.commission_lines_ids.unlink()
        self.update({'sale_commission_config_id': self.sale_commission_config_id.id,
                    'to_date': self.to_date,
                    'commission_lines_ids': commission_lines})
        # self.state = 'approved'

        # this line come outside every condition for confirmed ordes,confirmed invoices,paid invoices
