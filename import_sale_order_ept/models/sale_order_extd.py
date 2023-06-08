from odoo import fields, models



class SaleOrderExtd(models.Model):

   _inherit='sale.order'

   log_id=fields.Many2one(comodel_name='log.ept',string='Log',help='id of the log created for order.')