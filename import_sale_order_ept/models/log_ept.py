from odoo import fields, models, api
from datetime import date


class LogEpt(models.Model):
    _name = 'log.ept'
    _description = 'Log Ept'

    name = fields.Char(string='Name', help='name of the log')
    date = fields.Date(string='Date', default=date.today(), help='date of the log')
    log_lines_ids = fields.One2many(comodel_name='log.lines.ept', inverse_name='log_id', string='Log Lines',
                                    help='log lines ids  of the log')
    order_ids = fields.One2many(comodel_name='sale.order', inverse_name='log_id', string='Sale Order',
                                help='log lines ids  of the log')
    import_sale_order_ept_id = fields.Many2one(comodel_name='import.sale.order.ept', string='Imported Sale Order',
                                               help='Log id of the log lines ept')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.log.ept')
        return super(LogEpt, self).create(vals)

    def action_view_orders(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_orders')
        if len(self.order_ids) > 1:
            action['domain'] = [('id', 'in', self.order_ids.ids)]
        else:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = self.order_ids.id
        return action
