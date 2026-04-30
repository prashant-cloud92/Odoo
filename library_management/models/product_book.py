from odoo import api, fields, models, tools

class product_book(models.Model):
    _inherit = 'product.template'

    author_name = fields.Char("Author Name")
    available_qty = fields.Integer("Available Qty")
    is_available = fields.Boolean(compute="_book_available", store=True, string="Is Available")
    code = fields.Char("Book Code", default="123456")
    image_1920 = fields.Image("Book Image")

    @api.depends('available_qty')
    def _book_available(self):
        for rec in self:
            rec.is_available = rec.available_qty > 0


