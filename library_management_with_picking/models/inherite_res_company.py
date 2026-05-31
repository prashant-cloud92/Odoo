from odoo import api,fields,models
from odoo.api import ValuesType, Self
from odoo.fields import One2many, Many2one


class InheriteCompany(models.Model):
    _inherit = 'res.company'

    penalty_charge=fields.Integer(string="Penalty Charge",default=0)
    book_validity=fields.Integer(string="Book Validity",default=7)
    penalty_data=One2many('custom.penalty','company_id',string="Penalty")

    type_out = Many2one('stock.picking.type','Type Out')
    type_in = Many2one('stock.picking.type', 'Type In')


