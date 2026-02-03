# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bank Account Detail',
    'version': '1.0',
    'summary': 'Manages operation of Bank',
    'description':'Manages operation of Bank Account',
    'depends': ['base'],
    'data': [

        'views/bank_account_view.xml',
        'views/balance_transfer.xml',

        ],
    'installable': True,
}
