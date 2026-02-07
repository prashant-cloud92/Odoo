# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Sutter Extend',
    'version': '1.0',
    'summary': 'Sutter Extend',
    'description': "sutter extend",
    'description':'Manages operation of Bank Account',
    'depends': ['base','sale'],
    'data': [

        'views/sutter_extend.xml',
        'views/sale_line.xml',




        ],
    'installable': True,
}
