{
    'name': 'Employee Loan Management',
    'version': '0.1',
    'website' : 'www.mufti.ahmed',
    'category': 'Tools',
    'summary': 'This is a loan management  for employee',
    'description': """
""",
    'author': 'OpenERP SA',
    'depends': ['sale','hr'],
    'data': [
        'security/employee_loan_security.xml',
        'employee_loan_view.xml',
        'loan_details_view.xml',
        'loan_management/views/loan_common_view.xml',
        'loan_management/views/common_payment_schedule_view.xml',
        'loan_management/views/leih_loan_view.xml',
        'loan_management/views/loan_in_payment_view.xml',
        'PF/pf_opening_view.xml',
        'PF/pf_opening_view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'auto_install': False,
}