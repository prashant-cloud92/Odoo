from odoo import fields, models

class InterestSubject(models.Model):
    _name = 'interest.subject'
    _description = 'Interest Subject'
    _rec_name = 'interest_subject'

    interest_subject = fields.Char(string='Interest Subject')
    student_id = fields.Many2many('student.info','student_info_interest_subject_ref','interest_subject_id','student_id', string='Student')

