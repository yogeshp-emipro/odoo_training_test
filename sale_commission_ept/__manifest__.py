{
    'name': 'Sale Commission Ept',
    'version': '1.2',
    'aurthor': 'Yogesh Pandey',
    'description': 'This is sale commision module designed for learning purpose ...',
    'depends': ['crm', 'sale','mail','sale_management','purchase','account'],
    'data': ['security/sale_commission_ept_security.xml',
             'security/ir.model.access.csv',
             'views/sale_commission_config_view.xml',
             'views/sales_commission_ept_view.xml',
             'wizard/commission_recalculate_reason_wizard_view.xml',
             'views/sale_commission_ept_inherit_view.xml',
             'views/res_config_settings_view.xml']
}

