from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryBorrow(models.Model):
    _name = 'lib_mgmt.borrow'
    _description = 'Library Borrow Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
    book_id = fields.Many2one('lib_mgmt.book', string='Book', required=True, tracking=True)
    member_id = fields.Many2one('lib_mgmt.member', string='Member', required=True, tracking=True, default=lambda self: self._default_member())
    borrow_date = fields.Date(string='Borrow Date', required=True, default=fields.Date.context_today)
    return_date = fields.Date(string='Expected Return Date')
    actual_return_date = fields.Date(string='Actual Return Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('lib_mgmt.borrow') or 'New'
        return super(LibraryBorrow, self).create(vals_list)

    def _default_member(self):
        member = self.env['lib_mgmt.member'].search([('user_id', '=', self.env.uid)], limit=1)
        return member.id if member else False

    def action_borrow(self):
        for record in self:
            if record.book_id.available_copies <= 0:
                raise UserError("No copies of this book are currently available.")
            record.state = 'borrowed'

    def action_return(self):
        for record in self:
            record.state = 'returned'
            record.actual_return_date = fields.Date.today()
