from odoo import models, fields,api,Command


class SalePersonLeadCount(models.Model):
    _name = 'salesperson.lead.count'
    _description = 'Sale Person Lead Count'
    # sales person name
    # count number of pipeline of that salesperson

    # total revenue of those leads (which are in won stage only) - for given salesperson
    # total number of quotations created from those leads.
    # total number of sales orders created from those leads.
    # sum of total order amounts of all those sales orders.
    # percentage of conversation amount from expected revenue to sales order total amount.
    # Consider confirmed sales orders only, not quotations.
    name = fields.Char(string='SalePerson Name', help='Name of the saleperson')
    count_pipeline = fields.Integer(string='Pipeline Count', help='Pipeline count of the saleperson lead count')
    total_revenue = fields.Float(string='Total Revenue', help='total revenue of the saleperson lead count')
    total_quotation = fields.Integer(string='Total Quotation', help='number of quotation of the saleperson lead count')
    total_sale_order = fields.Integer(string='Total Sale Orders',
                                      help='number of sale orders of the saleperson lead count')
    total_order_amount = fields.Float(string='Total Order Amount',
                                      help='total order amount of the saleperson lead count')
    percentage_conversation_amt = fields.Integer(string='Percentage Convers',
                                                help='percentage conversation amount of the saleperson lead count')

    partner_lead_rel_id = fields.Many2one(comodel_name='partner.lead.rel', string='Partner Lead',
                                          help='Lead Partner id of the  partner lead rel')

