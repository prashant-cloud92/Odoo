# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Management',
    'version': '1.0',
    'summary': 'Project Management',
    'description':'Project Management',
    'depends': ['base'],
    'data': [
        'securities/security.xml',
        'securities/ir.model.access.csv',

        'views/customer_master.xml',
        'views/my_project.xml',
        'views/my_tasks.xml'

        ],
    'installable': True,
}
