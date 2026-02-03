from odoo import api, fields, models, tools
class StudentInfo(models.Model):
    _name = 'student.info'
    _description = 'Student Information'

    name = fields.Char(required=True)
    email = fields.Char()
    mobile = fields.Char()
    age = fields.Integer()
    fees = fields.Float()
    is_active = fields.Boolean(default=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])

    birth_date = fields.Date()
    join_datetime = fields.Datetime()

    image_1920 = fields.Image()

    address = fields.Text()
    # state = fields.Many2one('res.country.state')
    # subjects_ids = fields.Many2many('subject.master')
    # line_ids = fields.One2many('student.line', 'student_id')

    def action_confirm(self):
        for record in self:
            record.state = 'confirm'