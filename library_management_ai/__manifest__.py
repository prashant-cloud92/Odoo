{
    'name': 'AI Library Management',
    'version': '18.0.1.0.0',
    'category': 'Services/Library',
    'summary': 'Manage Library Books, Members and Borrowing',
    'description': """
Library Management System
=========================
Features:
- Manage Books
- Manage Members
- Track Book Borrowing
- User and Administrator access levels
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/book_views.xml',
        'views/member_views.xml',
        'views/borrow_views.xml',
        'views/library_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
