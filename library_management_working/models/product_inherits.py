from odoo import fields,models

class Product(models.Model):
    _inherit = "product.template"

    is_book=fields.Boolean("Is Book")