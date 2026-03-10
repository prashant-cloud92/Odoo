from odoo import api, fields, models, tools

class Country(models.Model):
    _name = 'country.detail'
    _rec_name = 'country_name'

    country_name=fields.Char(string='Country Name')

