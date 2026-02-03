from odoo import api, fields, models
class Country(models.Model):
    _name = 'country.table'
    name = fields.Char(required=True)
    state = fields.One2many('states.table','country_id_fk',required=True)