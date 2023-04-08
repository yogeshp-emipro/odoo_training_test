from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_ept_id = fields.Many2one(comodel_name='product.product', string='Product',
                                     help='id of the product', domain=[('detailed_type', '=', 'service')],config_parameter='sale_commission_ept.product_ept_id')