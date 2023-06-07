from odoo import models,fields

class LogDemoEPt(models.Model):
    _name='log.demo.ept'

    _log_access = False

    name=fields.Char(string='Log Name')
    date=fields.Date(string='Log Date',default=fields.Date.today())
#     126354670
