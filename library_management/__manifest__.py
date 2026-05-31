# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Library Management 2.0',
    'version': '1.0',
    'summary': 'Library Management 2.0',
    'description':'Library Management 2.0',
    'depends': ['base','product','stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/book_issue.xml',
        'views/library_book.xml',
        'views/custome_panalty.xml',
        'views/res_company_view.xml',
        'views/product.xml',
        'report/template_design.xml',
        'report/template_parent.xml',




        ],
    'installable': True,
}
