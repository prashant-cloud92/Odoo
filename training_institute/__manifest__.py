# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Training Institute Management',
    'version': '1.0',
    'summary': 'Training Institute Management',
    'description':'Training Institute Management',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/batch.xml',
        'views/course.xml',
        'views/student.xml',

        ],
    'installable': True,
}
