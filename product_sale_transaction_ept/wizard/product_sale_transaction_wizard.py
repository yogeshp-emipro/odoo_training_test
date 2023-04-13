from odoo import models, fields, Command


class ProductSaleTransactionWizard(models.TransientModel):
    _name = 'product.sale.transaction.wizard'
    _description = 'Product Sale Transaction Wizard'

    def create_sale_order(self):
        res = self.env.context.get('active_id', False)

        field_visit = self.env['field.visit.ept'].browse(res)
        print(field_visit)
        order_lines = []
        for fieldline in field_visit.field_visit_line_ids:

            product = fieldline.product_id
            order_lines.append(Command.create({'product_id': product.id,
                                               'uom_id': product.uom_id.id,
                                               'unit_price': product.price,
                                               'product_qty': fieldline.qty}))
        self.env['sale.order.ept'].create({'partner_id': field_visit.partner_id.id,
                                           'order_line_ids': order_lines})
