from email.policy import default

from odoo import api, fields, models, tools

class LibraryBook(models.Model):
    _name = 'library.book'


    name=fields.Char("Book Name")
    author_name=fields.Char("Author Name")
    available_qty=fields.Integer("Available Qty")
    is_available=fields.Boolean(compute="_book_available", store=True,string="Is Available")
    code=fields.Char("Book Code",default="123456")


    issue_book_count = fields.Integer(compute="_compute_issue",string="Issues")


    @api.depends('available_qty')
    def _book_available(self):
        for rec in self:
            rec.is_available = rec.available_qty > 0

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.code}] {rec.name}" if rec.code else rec.name

    def _compute_issue(self):
        issue_book=self.env['book.issue'].search([('book_id','=',self.id)])

        self.issue_book_count = len(issue_book)

    def action_open_documents(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Book Issue',
            'view_mode': 'list',
            'res_model': 'book.issue',

            'domain': [('book_id', '=', self.id)],
        }

