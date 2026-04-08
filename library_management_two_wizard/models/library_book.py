from odoo import api, fields, models, tools

class LibraryBook(models.Model):
    _name = 'library.book'


    name=fields.Char("Book Name")
    author_name=fields.Char("Author Name")
    available_qty=fields.Integer("Available Qty")
    is_available=fields.Boolean(compute="_book_available", store=True,string="Is Available")

    @api.depends('available_qty')
    def _book_available(self):
        for rec in self:
            rec.is_available = rec.available_qty > 0
