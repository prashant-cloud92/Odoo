# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Library Management working',
    'version': '2.0',
    'summary': 'Library Management 2.0',
    'description':'Library Management 2.0',
    'depends': ['base','product','stock'],
    'data': [

        'views/book_detail.xml',
        'views/book_issue.xml',
        'views/dashboard_action.xml',
        'reports/template_data.xml',
        'reports/template_design_new.xml',
        'data/crone_book.xml',






        ],
    'assets': {
        'web.assets_backend': [
            'library_management_working/static/src/js/book_dashboard.js',
            'library_management_working/static/src/js/book_dashboard_action.js',
            'library_management_working/static/src/xml/book_dashboard.xml',
        ],
    },
    'installable': True,
}
