from odoo import models, fields, api, Command


class PartnerLeadRel(models.Model):
    _name = 'partner.lead.rel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Partner Lead Rel'
    # name
    # from_date
    # to_date
    # partner_id (m2o of res.partner)
    # partner_contact_ids (m2m of res.partner)
    # salesperson_lead_count_ids (o2m of salesperson.lead.count)
    # lead_ids (m2m of crm.lead)
    # total_revenue
    name = fields.Char(string='Name', help='Name of the partner')

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
    lead_count = fields.Integer(string='Leads', compute='_compute_lead_count',
                                help='Number of lead/pipline of the partner')
    no_sale_order = fields.Integer(string='SaleOrder', compute='_compute_no_sale_order',
                                   help='Number of the saleorder correponding to the partner lead rel.')

    # domain="[('parent_id','in',lambda partner:partner.child_ids.parent_id.ids)]"

    # def _get_contacts(self):
    #     if self.partner_id:
    #         self.partner_contact_ids= self.partner_id.child_ids
    #     else:
    #         self.partner_contact_ids=self.env.user
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.partner.lead.rel')
        return super(PartnerLeadRel, self).create(vals)

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
                    pipeline = self.env['crm.lead'].search_count(
                        [('user_id', '=', lead.order_ids.mapped('user_id').id)])
                    saleperson_leads.append(Command.create({'name': lead.order_ids.mapped('user_id').name,
                                                            'total_revenue': lead.prorated_revenue,
                                                            'count_pipeline': pipeline,
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
                                    order_dict[order.user_id.id] = [
                                        order_dict.get(order.user_id.id)[0] + order.amount_total,
                                        order_dict.get(order.user_id.id)[1] + 1] if order_dict.get(
                                        order.user_id.id) else [order.amount_total, 0]
                                    # here if user with that id  is already present i.e sale person in already present in then we adding the sale order_amount and no_of_saleorder
                                else:
                                    quotation_dict[order.user_id.id] = quotation_dict.get(
                                        order.user_id.id) + 1 if quotation_dict.get(
                                        order.user_id.id) else 1  # here if user id is present but in draft state so we it count as quotation ,so we are increasing the quotation by 1 of it's previous quotation count
                            else:
                                sale_person.append(order.user_id.id)  # here we are appending user id in list.
                                if order.state == 'sale':
                                    order_dict[order.user_id.id] = [order.amount_total,
                                                                    1]  # appending list of amount and intially 1  as order_total_amount,No_sale_order
                                else:
                                    quotation_dict[
                                        order.user_id.id] = 1  # here if sale order in draft state then it will count as quotation intillay as 1

                    for order in order_dict:  # here order_dict is dictionary of that contain order_amount_total and no_sale_order_count, iterating on the key of the i.e user id
                        result = self.env['crm.lead'].search_count([('user_id', '=', order)])
                        saleperson_leads.append(Command.create({'name': self.env['res.users'].browse(order).name,
                                                                'total_revenue': lead.expected_revenue,
                                                                'count_pipeline': result,
                                                                'total_quotation': quotation_dict.get(order),
                                                                'total_sale_order': order_dict[order][1],
                                                                'total_order_amount': order_dict[order][0],
                                                                'percentage_conversation_amt': lead.probability
                                                                }))

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

    @api.depends('lead_ids')
    def _compute_lead_count(self):
        for lead in self:
            lead.lead_count = len(lead.lead_ids)

    def action_view_leads(self):
        action = self.env["ir.actions.actions"]._for_xml_id("crm.crm_lead_all_leads")
        kanban = self.env.ref('crm.view_crm_lead_kanban').id
        form = self.env.ref('crm.crm_lead_view_form').id
        action['views'] = [(kanban, 'kanban'), (form, 'form')]
        action['domain'] = [('id', 'in', self.lead_ids.ids)]
        return action

    @api.depends('lead_ids')
    def _compute_no_sale_order(self):
        for lead in self:
            lead.no_sale_order = len([order.order_ids for order in lead.lead_ids])

    def action_open_sale_order(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale.action_sale_order_form_view')
        tree = self.env.ref('sale.view_quotation_tree_with_onboarding').id
        form = self.env.ref('sale.view_order_form').id
        action['views'] = [(tree, 'tree'), (form, 'form')]
        orders = self.lead_ids.order_ids.filtered(
            lambda order: order.state not in 'draft' and order.mapped('picking_ids.state') not in ['done'])
        action['domain'] = [('id', 'in', orders.ids)]
        return action

    def search(self, args, offset=0, limit=None, order=None, count=False):

        if len(args):
            if args[0][0] == 'name':
                args.insert(0, '|')
                args.append(['partner_id', 'ilike', args[1][2]])

        return super(PartnerLeadRel, self).search(args, offset, limit, order, count)
