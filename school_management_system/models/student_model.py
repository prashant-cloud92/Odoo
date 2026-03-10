from odoo import fields, models

class SchoolStudent(models.Model):
    _name = 'student.model'

    name = fields.Char()

    subject_ids = fields.Many2many('subject.model', string="Subjects")

    teacher_ids = fields.Many2one('teacher.model',related='subject_ids.teacher_id', string="Teachers")

    teacher_id = fields.Many2one('teacher.model', string="Teacher")



    batch_line_ids = fields.One2many(
        'batch.model',
        'student_id',
        string="Batch Subjects"
    )
