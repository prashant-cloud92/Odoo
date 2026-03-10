from email.policy import default

from odoo import models, api, fields


class Course(models.Model):
    _name = 'training.course'
    _description = 'Training Course'


    name=fields.Char("Course Name")
    fees=fields.Float("Fees")
    duration_days=fields.Integer("Duration Days")
    is_active=fields.Boolean("Is Active",default=False)
    level=fields.Selection(selection=[('beginner', 'Beginner'),
                            ('intermediate','Intermediate'),
                            ('advance','Advanced')],
                            string='Course Level')
    batch_ids=fields.Many2many('training.batch',string="Batches")
    student_ids=fields.Many2many('training.student',string="Students")