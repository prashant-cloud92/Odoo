from odoo import api, fields, models, tools

class CustomerMaster(models.Model):

    _name = 'customer.master'
    _description = 'Customer Master'

    name=fields.Char(string='Customer Name')
    company_name=fields.Char(string='Company Name')
    city=fields.Char(string='City')
    mobile=fields.Char(string='Mobile')
    email=fields.Char(string='Email')

