from odoo import fields, models

class Transport(models.Model):
    _inherit = "res.partner"

    transport_company=fields.Char(string=" Transport Company")