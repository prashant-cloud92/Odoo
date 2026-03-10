from odoo import fields,models

class MyProject(models.Model):
    _name='my.project'
    _description='My Project'

    name=fields.Char(string='Project Name')
    customer_id=fields.Many2one('customer.master',string='Customer')
    budget=fields.Float(string='Budget')
    is_active=fields.Boolean(string='Is Active')
    task_ids=fields.One2many('my.task','project_id',string='Tasks')

    member_ids=fields.Many2many('res.users',string='Members')