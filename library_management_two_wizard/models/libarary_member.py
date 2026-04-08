from odoo import api, fields, models, tools

class LibraryMember(models.Model):

    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Many2one('res.users',string='Name')
    email = fields.Char(string='Email')
    is_active = fields.Boolean(string='Is Active')