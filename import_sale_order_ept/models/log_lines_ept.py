from odoo import fields, models


class LogLinesEpt(models.Model):
    _name = 'log.lines.ept'
    _description = 'Log Lines Ept'

    message = fields.Text(string='Message', help='message of the log')
    message_type = fields.Selection(string='Message Type',
                                    selection=[('success', 'Success'), ('failure', 'Failure'), ('warning', 'Warning')],
                                    help='message type of the log')
    log_id = fields.Many2one(comodel_name='log.ept', string='Log', help='Log id of the log lines ept')

