{
   'name' : 'Inventory Reports Custom',
   'version' : '1.0',
   'author' : 'TamkeenTech',
   'summary' : 'Additional Reports for Warehouse Module',
   'description' : """ 
    This Module Contains :
     1- Inventory Report which display Products Qtys.
   """,
   'depends' : ['stock'],
   'data' : [
           'security/security.xml',
           'views/reports_view.xml',
           'wizard/incoming_outgoing_report.xml',
           'report/incoming_outgoing_template.xml',
           'report/incoming_outgoing_price_template.xml',


   ],
   'installable' : True,
   'application' : False,
}
