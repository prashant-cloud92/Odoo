from odoo import models,fields,api

class Batch(models.Model):
    _name = 'training.batch'
    _description = 'Training Batch'


    name=fields.Char("Batch Name")
    course_id=fields.Many2one('training.course',string="Course")
    start_date=fields.Date("Start Date")
    end_date=fields.Date("End Date")
    capacity=fields.Integer("Capacity")
    student_ids=fields.One2many('training.student','batch_ids',string="Select Students")