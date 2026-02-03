from odoo import api, fields, models, tools

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_details2=fields.Char("Product Details")
