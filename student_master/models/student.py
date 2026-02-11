from odoo import models, fields, api
from odoo.api import ValuesType, Self


class Student(models.Model):
    _name = 'student.detail'
    _rec_name = 'first_name'

    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    surname = fields.Char("Surname")
    birth_date = fields.Date("Birth Date")
    email = fields.Char("Email")
    mobile = fields.Char("Mobile")

    def create(self, vals):

        vals['first_name']='praaaa'
        return super(Student,self).create(vals)
