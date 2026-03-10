from odoo import fields,models

class MyTasks(models.Model):
    _name='my.task'
    _description='Tasks'

    task_name=fields.Char(string='Task Name')
    project_id=fields.Many2one('my.project',string='Project')

    project_member_id=fields.Many2many('res.users',related='project_id.member_ids')
    assigned_to_id=fields.Many2one('res.users',string='Assigned To')
    priority=fields.Selection(selection=[('low','Low'),('medium','Medium'),('high','High')],string='Priority')
    estimated_hours=fields.Integer(string='Estimated Hours')
    status=fields.Selection(selection=[('new','New'),('in_progress','In Progress'),('done','Done')],string='Status')




