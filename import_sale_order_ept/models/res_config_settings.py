from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    shipping_product = fields.Many2one(comodel_name='product.template', string="Shipping Product",
                                       domain=[('detailed_type', '=', 'service')], help='this is shipping product ',
                                       config_parameter='import_sale_order_ept.shipping_product')
