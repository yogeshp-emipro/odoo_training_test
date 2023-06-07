{
    'name': 'SaleOrderEpt',
    'description': 'This is sale order ept module to import the sales data from csv files.',
    'depends': ['sale', 'sales_team'],
    'data': ['security/ir.model.access.csv',
             'data/sequence.xml',
             'views/res_config_settings_views.xml',
             'views/log_ept_view.xml',
             'views/import_sale_order_ept_view.xml',
             'views/log_demo_ept_view.xml']

}
#
# sequence.xml
