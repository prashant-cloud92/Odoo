from odoo import models, fields, api

class LibraryMember(models.Model):
    _name = 'lib_mgmt.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Related User', help="User associated with this member for login.")
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    borrow_ids = fields.One2many('lib_mgmt.borrow', 'member_id', string='Borrowed Books')
    active = fields.Boolean(default=True)
