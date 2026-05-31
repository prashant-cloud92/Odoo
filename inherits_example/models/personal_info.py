from odoo import api, fields, models, tools

class PersonalInfo(models.Model):
    _name = 'personal.info'
    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")