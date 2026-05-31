from odoo import api, fields, models, tools

class company_emp(models.Model):
    _name = 'company.employee'
    _inherits = {'personal.info':'personal_id'}

    personal_id = fields.Many2one('personal.info',ondelete='cascade')

    emp_id=fields.Char("Employee ID")
    department=fields.Char("Department")
