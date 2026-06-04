from odoo import fields,models

class StudentData(models.Model):
    _name = 'student.data'

    name=fields.Char("name")
    email=fields.Char("email")
    contact_no=fields.Char("contact number")
