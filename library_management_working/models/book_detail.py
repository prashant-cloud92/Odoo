from odoo import api,fields,models,tools

class BookDetail(models.Model):
    _name = 'book.detail'
    _description = 'Book Detail'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Book Name")
    product_id = fields.Many2one('product.product',string='Product')
    author_name = fields.Char("Author Name")
    available_qty = fields.Integer("Available Qty")
    is_available = fields.Boolean(compute="_book_available", store=True, string="Is Available")

    def crone_job_low_stock_book(self):
        books=self.search([('available_qty','<',5)])
        if books:

            users = self.env['res.users'].search([])

            for book in books:
                for user in users:
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref(
                            'mail.mail_activity_data_todo'
                        ).id,
                        'note': f"{book.name} stock is low ({book.available_qty})",
                        'user_id': user.id,
                        'res_id': book.id,
                        'res_model_id': self.env['ir.model']._get_id('book.detail'),
                    })

    @api.depends('available_qty')
    def _book_available(self):
        for record in self:
            if record.available_qty>0:
                record.is_available = True
            else:
                record.is_available = False

    @api.model
    def create(self, vals):
        book = super().create(vals)

        product_template = self.env['product.template'].create({
            'name': book.name,
            'is_book': True,
            'is_storable': True,
        })

        product_varient = product_template.product_variant_id

        book.product_id = product_varient.id

        stock_location = self.env.ref('stock.stock_location_stock')

        self.env['stock.quant'].create({
            'product_id': product_varient.id,
            'location_id': stock_location.id,
            'inventory_quantity': book.available_qty,
        }).action_apply_inventory()

        return book