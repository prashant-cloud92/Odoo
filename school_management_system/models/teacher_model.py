from odoo import api, fields, models, tools, _

class TeacherModel(models.Model):
    _name = 'teacher.model'
    _description = 'Teacher Model'

    name = fields.Char("Teacher Name")
    subject_id=fields.One2many('subject.model','teacher_id','Teacher Subjects')
