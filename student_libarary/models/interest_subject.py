from odoo import fields, models

class InterestSubject(models.Model):
    _name = 'interest.subject'
    _description = 'Interest Subject'
    _rec_name = 'interest_subject'

    interest_subject = fields.Char(string='Interest Subject')
    student_id = fields.Many2many('student.info','interest_subject_student_info_rel','interest_subject_id','student_info_id', string='Student')

