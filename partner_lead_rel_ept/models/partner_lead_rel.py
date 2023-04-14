from odoo import models, fields, api, Command


class PartnerLeadRel(models.Model):
    _name = 'partner.lead.rel'
    _description = 'Partner Lead Rel'
    # name
    # from_date
    # to_date
    # partner_id (m2o of res.partner)
    # partner_contact_ids (m2m of res.partner)
    # salesperson_lead_count_ids (o2m of salesperson.lead.count)
    # lead_ids (m2m of crm.lead)
    # total_revenue
    name = fields.Char(string='Partner Name', help='Name of the partner')

    from_date = fields.Date(string='Lead From Date', required=True, default=fields.Date.today(),
                            help="from date of the partner lead rel.")
    to_date = fields.Date(string='Lead To Date', required=True, help="to date of the partner lead rel.")

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', domain="[('is_company','=',True)]",
                                 help='Partner of the  partner lead rel')

    partner_contact_ids = fields.Many2many(comodel_name='res.partner', string='Partner Contacts',
                                           domain="[('parent_id','=',partner_id)]",
                                           help='Contact ids of the Partner')
    salesperson_lead_count_ids = fields.One2many(comodel_name='salesperson.lead.count',
                                                 inverse_name='partner_lead_rel_id',
                                                 string='Field Visit Line Ids', ondelete='cascade',
                                                 help='field visit line ids of field visit ept')

    lead_ids = fields.Many2many(comodel_name='crm.lead', string='Leads',
                                domain="['|',('partner_id','=',partner_id),('partner_id','in','partner_contact_ids')]",
                                help='Lead ids of the partner lead rel')
    total_revenue = fields.Float(string='Total Revenue', compute='_compute_total_revenue',
                                 help='total revenue of the partner lead rel')
    # domain="[('parent_id','in',lambda partner:partner.child_ids.parent_id.ids)]"

    # def _get_contacts(self):
    #     if self.partner_id:
    #         self.partner_contact_ids= self.partner_id.child_ids
    #     else:
    #         self.partner_contact_ids=self.env.user

    def get_pipeline_details(self):
        print(self.lead_ids)
        # prorated_revenue,quotation_count,
        # sale_order_count,sale_amount_total
        # self.lead_ids.order_ids.mapped('user_id').name
        # self.lead_ids.stage_id.display_name
        # 'probability
        saleperson_leads = []
        sale_person = []

        for lead in self.lead_ids:
            if lead.stage_id.display_name == 'Won':

                if len(lead.order_ids.mapped('user_id')) <= 1:
                    result = self.env['crm.lead'].search_count([('user_id', '=', lead.order_ids.mapped('user_id').id)])
                    saleperson_leads.append(Command.create({'name': lead.order_ids.mapped('user_id').name,
                                                            'total_revenue': lead.prorated_revenue,
                                                            'count_pipeline':result,
                                                            'total_quotation': lead.quotation_count,
                                                            'total_sale_order': lead.sale_order_count,
                                                            'total_order_amount': lead.sale_amount_total,
                                                            'percentage_conversation_amt': lead.probability
                                                            }))
                else:
                    order_dict = {}
                    quotation_dict = {}

                    for order in lead.order_ids:
                        if order.state in ['draft', 'sale']:
                            if order.user_id.id in sale_person:
                                if order.state == 'sale':
                                    order_dict[order.user_id.id] = [order_dict.get(order.user_id.id)[0] + order.amount_total,order_dict.get(order.user_id.id)[1]+1] if order_dict.get(order.user_id.id) else [order.amount_total,0]
                                else:
                                    quotation_dict[order.user_id.id] = quotation_dict.get(order.user_id.id) + 1 if quotation_dict.get(order.user_id.id) else 1
                            else:
                                sale_person.append(order.user_id.id)
                                if order.state == 'sale':
                                    order_dict[order.user_id.id] = [order.amount_total,1]
                                else:
                                    quotation_dict[order.user_id.id] = 1

                    for order in order_dict:
                        result=self.env['crm.lead'].search_count([('user_id', '=', order)])
                        saleperson_leads.append(Command.create({'name': self.env['res.users'].browse(order).name,
                                                                'total_revenue': lead.expected_revenue,
                                                                'count_pipeline': result,
                                                                'total_quotation': quotation_dict.get(order),
                                                                'total_sale_order': order_dict[order][1],
                                                                'total_order_amount': order_dict[order][0],
                                                                'percentage_conversation_amt': lead.probability
                                                                }))
                    print(order_dict)

        self.salesperson_lead_count_ids.unlink()
        self.write({'salesperson_lead_count_ids': saleperson_leads})

    def _compute_total_revenue(self):
        for lead in self:
            # total_rev = 0
            # for order in lead.salesperson_lead_count_ids:
            #     total_rev += order.prorated_revenue
            # lead.total_revenue = total_rev

            lead.total_revenue = sum([order.expected_revenue for order in lead.lead_ids])
        print(self.partner_contact_ids)

    def view_leads(self):
        pass