from odoo import fields, models

class BillboardType(models.Model):
    _name = 'billboard.type'
    _description = 'Billboard Type'

    name = fields.Char(string='Type Name', required=True)
    parent_id = fields.Many2one('billboard.type', string='Parent Category', index=True, ondelete='cascade')
    property_definitions = fields.PropertiesDefinition(string='Billboard Properties')
