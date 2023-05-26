from odoo import fields, models
from datetime import date
import csv
import base64
from io import StringIO


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
        print(headers)
        #['Order No', 'Order Date', 'Currency', 'Customer Code',
        # 'Name', 'Email', 'Product Description', 'SKU', 'Quantity', 'Price',
        # 'Cost Per Unit', 'Shipping Charge', 'Shipping Paid To Carrier']
        for row in csv_reader:
            order_no=row['Order No']
            if self.env['sale.order'].search([('name','=',order_no)]):
                print('order no is present')
            else:
                print(row)


