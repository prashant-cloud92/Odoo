from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'lib_mgmt.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, tracking=True)
    author = fields.Char(string='Author', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', tracking=True)
    copies = fields.Integer(string='Total Copies', default=1, required=True)
    available_copies = fields.Integer(string='Available Copies', compute='_compute_available_copies', store=True)
    borrow_ids = fields.One2many('lib_mgmt.borrow', 'book_id', string='Borrowings')
    active = fields.Boolean(default=True)

    @api.depends('copies', 'borrow_ids.state')
    def _compute_available_copies(self):
        for book in self:
            borrowed_count = len(book.borrow_ids.filtered(lambda b: b.state == 'borrowed'))
            book.available_copies = book.copies - borrowed_count
