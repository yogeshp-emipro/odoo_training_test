from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError, UserError
from lxml import etree
import json
import simplejson


class SalesCommissionEpt(models.Model):
    _name = 'sales.commission.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _descripiton = 'Sales Commission Ept'

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
                                           string='Sale Commission Line ', ondelete='cascade',
                                           help='sale commission line of sale commission ept')
    total_commission = fields.Float(string=' Total Commission', compute='_compute_total_commission',
                                    help=' total commission of the sale commission')
    amount_residual = fields.Float(string=' Amount Remaining',
                                   help='amount remaining of the sale commission')
    commission_final_paid_date = fields.Datetime(string='Commission Paid Date', readonly=True,
                                                 default=fields.Datetime.now, help="paid date of the sale commission.")
    invoice_count = fields.Float(string='Invoices', compute='_compute_invoice_count')

    invoice_ids = fields.One2many(comodel_name='account.move',inverse_name='commission_id', string='Commission Invoices',
                                  help='invoice ids of the commissions')

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

            if self.commission_calculate_for == 'sale person' and self.user_id:
                sale_orders = self.env['sale.order'].search([('user_id', '=', self.user_id.id)])
            else:
                if self.sale_commission_config_id.sale_manager_commission_based_on == 'individual sales':
                    sale_orders = self.env['sale.order'].search([('user_id', '=', self.team_id.alias_user_id.id)])
                else:
                    sale_orders = self.env['sale.order'].search([('user_id', 'in', self.team_id.member_ids.ids)])

            old_state, new_state = self.state, 'approved'
            self.state = 'approved'

        elif self.sale_commission_config_id.commission_calculation_type == 'confirmed invoices':

            if self.commission_calculate_for == 'sale person' and self.user_id:
                sale_orders = self.env['sale.order'].search(
                    [('user_id', '=', self.user_id.id), ('invoice_ids.payment_state', '=', 'not_paid')])
            else:
                if self.sale_commission_config_id.sale_manager_commission_based_on == 'individual sales':
                    sale_orders = self.env['sale.order'].search([('user_id', '=', self.team_id.alias_user_id.id),
                                                                 ('invoice_ids.payment_state', '=', 'not_paid')])
                else:
                    sale_orders = self.env['sale.order'].search([('user_id', 'in', self.team_id.member_ids.ids),
                                                                 ('invoice_ids.payment_state', '=', 'not_paid')])
            old_state = self.state
            new_state = self.state = 'in-payment'

        else:
            if self.commission_calculate_for == 'sale person' and self.user_id:
                sale_orders = self.env['sale.order'].search(
                    [('user_id', '=', self.user_id.id), ('invoice_ids.payment_state', '=', 'paid')])
            else:
                if self.sale_commission_config_id.sale_manager_commission_based_on == 'individual sales':
                    sale_orders = self.env['sale.order'].search([('user_id', '=', self.team_id.alias_user_id.id),
                                                                 ('invoice_ids.payment_state', '=', 'paid')])
                else:
                    sale_orders = self.env['sale.order'].search([('user_id', 'in', self.team_id.member_ids.ids),
                                                                 ('invoice_ids.payment_state', '=', 'paid')])
            old_state = self.state
            new_state = self.state = 'paid'

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

        message = 'Status: %s --> %s' % (old_state, new_state)
        self.message_post(body=message)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sales.commission.ept',
            'res_id': self.id,
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'form_view_ref': 'sales.commission.ept_form_readonly'},
            'target': 'main',
        }

    @api.depends()
    def _compute_total_commission(self):

        for commission in self:
            total_commission = 0
            for comm in commission.commission_lines_ids:
                total_commission += comm.to_be_paid_commission_amount
            commission.total_commission = total_commission

    def generate_bill(self):
        invoice_lines = []
        product = self.env['product.product'].browse(
            int(self.env['ir.config_parameter'].get_param('sale_commission_ept.product_ept_id')))
        res = {
            'display_type': 'line_section',
            'product_id': product.id,
            'quantity': 1,
            'price_unit': product.price,
            'price_subtotal': self.total_commission
        }
        invoice_lines.append(Command.create(res))
        vals = {
            'partner_id': self.user_id.id if self.commission_calculate_for == 'sale person' and self.user_id else self.team_id.alias_user_id.id,
            'commission_id': self.id,
        }
        bill = self.env['account.move'].create(vals)
        res.setdefault('move_id', bill.id)
        print(res)
        bill.write({'invoice_line_ids': invoice_lines})
        print(bill.invoice_line_ids)

        # old_state = self.state
        # self.state = 'in-payment'
        # message = 'Status: %s --> %s' % (old_state, self.state)
        # self.message_post(body=message)

    def cancel_commission(self):
        if self.state in ['draft', 'approved']:
            self.state = 'cancelled'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sales.commission.ept',
            'res_id': self.id,
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'form_view_ref': 'sales.commission.ept_form_readonly'},
            'target': 'main',
        }

    def unlink(self):
        if self.state in ['approved', 'in-payment', 'paid']:
            raise ValidationError('Warning ! Commission cannot be deleted.')
        self.commission_lines_ids.unlink()
        return super(SalesCommissionEpt, self).unlink()

    def _compute_invoice_count(self):
        for commission in self:
            commission.invoice_count =len(commission.invoice_ids)

    def action_open_invoices(self):
         action = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
         if len(self.invoice_ids) > 1:
                action['domain'] = [('id', 'in', self.invoice_ids.ids)]

         else:
                form_view = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
                action['views'] = form_view
                action['res_id'] = self.invoice_ids.id
         return action
