from odoo import api, fields, models, tools


class City(models.Model):
    _name = 'city.detail'
    _rec_name = 'city_name'

    city_name = fields.Char(string='City Name')
    country_name=fields.Many2many('country.detail','country_city_rel','city_id','country_id',string="Country Names")
