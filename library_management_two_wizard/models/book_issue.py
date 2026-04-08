from Tools.scripts.dutree import store

from odoo import api,fields,models
from odoo.exceptions import UserError


class BookIssue(models.Model):
    _name = 'book.issue'
    _description = 'Book Issue'

    book_id = fields.Many2one("library.book",string="Book Name")
    member_id = fields.Many2one("library.member",string="Member Name")
    issue_date = fields.Datetime(string="Issue Date",default=fields.Date.today)
    return_date = fields.Datetime(string="Return Date",default=fields.Date.today)
    status = fields.Selection([('draft','Draft'),('issue','Issue'),('returned','Return')],default='draft', tracking=True,string="Status")
    days_issued = fields.Integer(compute='days_calculate',string="Days Issued",store=False)


    def create(self,vals):

        #vals['status'] = 'issue'
        record = super().create(vals)
        if not record.member_id.is_active:
            raise UserError("Please Active Your Account First")
        if record.book_id:
            if record.book_id.available_qty <= 0:
                raise UserError("Book is not available!")

            record.book_id.write({'available_qty':record.book_id.available_qty -1})
        return record

    @api.depends('issue_date','return_date')
    def days_calculate(self):
        for rec in self:
            rec.days_issued=0
            if rec.issue_date and rec.return_date:
                diff=(rec.return_date - rec.issue_date).days + 1
                rec.days_issued=diff


    def action_issue(self):
        for rec in self:
            if rec.book_id.available_qty <= 0:
                raise UserError("Book is not available!")
            rec.book_id.write({'available_qty':rec.book_id.available_qty -1})
            rec.write({'status':'issue'})

    def action_return(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Book',
            'res_model': 'return.book.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id
            }
        }

class ReturnBookWizard(models.TransientModel):
    _name = 'return.book.wizard'

    return_date = fields.Date(string="Return Date", default=fields.Date.today,required=True)
    issue_days=fields.Integer()


    def action_confirm_return(self):

        record=self.env['book.issue'].browse([self.env.context.get('active_id')])

        if not self.return_date:
            raise UserError("Please Select Return Date")

        record.book_id.write({'available_qty':record.book_id.available_qty+1})
        record.write({'status':'returned','return_date':self.return_date})

    def open_date_wizard(self):

            return {
                'type': 'ir.actions.act_window',
                'name': 'Select Date',
                'res_model': 'date.wizard',
                'view_mode': 'form',
                'target': 'new',  # popup
                'context': {'wizard_id': self.id},
            }

class DateWizard(models.TransientModel):
    _name = 'date.wizard'
    selected_date = fields.Date(string="Return Date", default=fields.Date.today,required=True)
    def action_apply_date(self):

        wizard_one_id = self.env.context.get('wizard_id')

        if not wizard_one_id:
            return {'type': 'ir.actions.act_window_close'}

        wizard_one = self.env['return.book.wizard'].browse(wizard_one_id)
        wizard_one.return_date = self.selected_date
        return {'type': 'ir.actions.act_window_close'}
    # def action_return(self):
    #     for rec in self:
    #         rec.status = 'return'
    #
    # def action_submit(self):
    #     for rec in self:
    #         rec.status = 'issue'
    #
    # def action_reset(self):
    #     for rec in self:
    #         rec.status = 'draft'