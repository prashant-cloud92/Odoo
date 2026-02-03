from odoo import api, fields, models, tools
class StudentInfo(models.Model):
    _name = 'student.info'
    _description = 'Student Information'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')

    address = fields.Char(string='Address')
    mobile = fields.Char(string='Mobile')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    birth_date = fields.Date()
    interest_subject = fields.Many2many('interest.subject',string='Interest Subject')