from odoo import fields, models
from datetime import date


class LogEpt(models.Model):
    _name = 'log.ept'
    _description = 'Log Ept'

    name = fields.Char(string='Name', help='name of the log')
    date = fields.Date(string='Date', default=date.today(), help='date of the log')
    log_lines_ids = fields.One2many(comodel_name='log.lines.ept', inverse_name='log_id', string='Log Lines',
                                    help='log lines ids  of the log')
