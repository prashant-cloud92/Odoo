from odoo import api, fields, models, tools

class Student(models.Model):
    _name = 'student.admission'
    _description = 'Student Admission'
    name = fields.Char(string='Name')
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                            ('approved', 'Approved'),
                            ('rejected', 'Rejected')], string="Status", default='draft', tracking=True)
    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

    def action_reset(self):
        self.state = 'draft'