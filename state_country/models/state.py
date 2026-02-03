from odoo import api, fields, models, tools
class Country(models.Model):
    _name = 'states.table'

    name = fields.Char(required=True)
    country_id_fk = fields.Many2one('country.table')