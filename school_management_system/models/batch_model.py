from odoo import fields, models

class SchoolBatchLine(models.Model):
    _name = 'batch.model'

    student_id = fields.Many2one('student.model')
    subject_id = fields.Many2one('subject.model')