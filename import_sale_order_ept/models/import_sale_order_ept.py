from odoo import fields, models
from datetime import date
import csv
import base64
from io import StringIO
from odoo import api, Command
from datetime import datetime, timezone


class ImportSaleOrderEpt(models.Model):
    _name = 'import.sale.order.ept'
    _description = 'Import Sale Order Ept'

    file_name = fields.Char(string='Name')
    choose_file = fields.Binary(string="Select File")
    date = fields.Date(string='Date', default=date.today(), help='date of the import sale order ept')
    log_lines_ids = fields.One2many(comodel_name='log.lines.ept', inverse_name='import_sale_order_ept_id',
                                    string='Log Lines',
                                    help='log lines ids  of the import sale order ept')

    def import_sale_order(self):
        try:
            data = StringIO(base64.b64decode(self.choose_file).decode())
        except Exception:
            data = StringIO(base64.b64decode(self.choose_file).decode('ISO-8859-1'))
        content = data.read()
        delimiter = ('\t', csv.Sniffer().sniff(content.splitlines()[0]).delimiter)[bool(content)]
        csv_reader = csv.DictReader(content.splitlines(), delimiter=delimiter)
        headers = csv_reader.fieldnames
        # print(headers)
        # ['Order No', 'Order Date', 'Currency', 'Customer Code',
        # 'Name', 'Email', 'Product Description', 'SKU', 'Quantity', 'Price',
        # 'Cost Per Unit', 'Shipping Charge', 'Shipping Paid To Carrier']
        for row in csv_reader:
            order_no = row['Order No']
            if self.env['sale.order'].search([('name', '=', order_no)]):
                print('order no is present')
            else:
                currency = self.env['res.currency'].search([('name', '=', row['Currency'])])

                if self.env['res.partner'].search([('customer_partner_code', '=', row['Customer Code'])]) and self.env[
                    'product.product'].search([('default_code', '=', row['SKU'])]) and currency and self.env[
                    'product.pricelist'].search([('currency_id', '=', currency.id)]):

                    partner = self.env['res.partner'].search([('customer_partner_code', '=', row['Customer Code'])])

                    product = self.env['product.product'].search([('default_code', '=', row['SKU'])])

                    new_pricelist = self.env['product.pricelist'].search([('currency_id', '=', currency.id)], limit=1)

                else:
                    if self.env['res.partner'].search([('customer_partner_code', '=', row['Customer Code'])]):
                        partner = self.env['res.partner'].search([('customer_partner_code', '=', row['Customer Code'])])
                    else:
                        partner = self.env['res.partner'].create({'name': row['Name'], 'email': row['Email'],
                                                                  'customer_partner_code': row[
                                                                      'Customer Code']})  # creating the partner if partner record is not there

                    if self.env['product.product'].search([('default_code', '=', row['SKU'])]):
                        product = self.env['product.product'].search([('default_code', '=', row['SKU'])])
                    else:
                        product = self.env['product.product'].create(
                            {'name': row['Product Description'], 'default_code': row['SKU'],
                             'list_price': row['Cost Per Unit'], })
                    # creating the product if product with that sku is not present in product template

                    # here we have taken if and else many time for product,partner,pricelist bcz it may possible that some time only product,partner,pricelist is present and few of their combination is not present.
                    pricelist = self.env['product.pricelist'].search([('currency_id', '=', currency.id)])

                    new_pricelist = pricelist if pricelist else self.env[
                        'product.pricelist'].create(
                        {'name': currency.name + 'pricelist', 'currency_id': currency.id})

                order_lines = Command.create(
                    {'product_id': product.id, 'cost_price': row['Cost Per Unit']})

                timestamp_str = row['Order Date']
                date = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S+00:00')

                self.env['sale.order'].create({'name': order_no,
                                               'date_order': date,
                                               'partner_id': partner.id,
                                               'partner_invoice_id': partner.id,
                                               'partner_shipping_id': partner.id,
                                               'pricelist_id': new_pricelist.id,
                                               'amount_total':row['Price'],
                                               'order_line': [order_lines]})

        # next to do what take the currency and check wheather any price list exist with that currency or not if not the create the pricelist with that creating the partner if partner record is not there
