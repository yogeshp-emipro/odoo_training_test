from odoo import fields, models,api
from datetime import date


class LogEpt(models.Model):
    _name = 'log.ept'
    _description = 'Log Ept'

    name = fields.Char(string='Name', help='name of the log')
    date = fields.Date(string='Date', default=date.today(), help='date of the log')
    log_lines_ids = fields.One2many(comodel_name='log.lines.ept', inverse_name='log_id', string='Log Lines',
                                    help='log lines ids  of the log')
    order_ids=fields.One2many(comodel_name='sale.order', inverse_name='log_id', string='Log Lines',
                                    help='log lines ids  of the log')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.log.ept')
        print('create is called...................',vals)
        return super(LogEpt, self).create(vals)