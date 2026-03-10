from odoo import models,fields,api

class Student(models.Model):
    _name = 'training.student'
    _description = 'Training Student'


    name=fields.Char("Student Name")
    email=fields.Char("Student Email")
    phone=fields.Char("Student Phone")
    age=fields.Char("Student Age")
    gender=fields.Selection(selection=[('Male','Male'),('Female','Female')],string="Student Gender")
    course_ids=fields.Many2many('training.course',string="Course")
    batch_ids=fields.Many2one('training.batch',string="Batch")

