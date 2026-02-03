from odoo import api, fields, models, tools
class CustomerTag(models.Model):
    _name = 'customer.tag'
    _rec_name = 'tag_name'

    tag_name= fields.Char(string="Category Name")
    select_company=fields.Many2many(
        'bank.account','bank_account_customer_tag_rel','customer_tag_id','bank_account_id',string="Company")
