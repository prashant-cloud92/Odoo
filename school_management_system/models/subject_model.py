from odoo import api, fields, models, tools, _

class SubjectModel(models.Model):
    _name = 'subject.model'
    _description = 'Subject Model'

    name = fields.Char()
    teacher_id = fields.Many2one('teacher.model')