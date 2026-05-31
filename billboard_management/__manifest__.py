{
    'name': 'Billboard Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage Billboards with customizable dynamic properties.',
    'description': """
        This module allows users to manage billboards with fully customizable properties based on the billboard type.
        For example, a Black Board can have 4 fields while a White Board can have 7 fields.
        Supports text, checkbox, selection, and more dynamically.
    """,
    'author': 'Antigravity',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/billboard_demo.xml',
        'views/billboard_type_views.xml',
        'views/billboard_board_views.xml',
        'views/billboard_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
