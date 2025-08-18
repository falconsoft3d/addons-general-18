{
    'name': 'Employee Portal MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','hr','project'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/hr_employee_views.xml',
        'views/project_project_views.xml',

        'views/portal_documentation_views.xml',
        'views/portal_photo_views.xml',
        'views/portal_improvement_views.xml',
        'views/portal_vacation_views.xml',
        'views/portal_complaint_views.xml',


        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'data/ir_sequence.xml',
    ],
    'license': 'LGPL-3',
}