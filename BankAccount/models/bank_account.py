from odoo import models,fields
from odoo.exceptions import UserError


class BankAccount(models.Model):
    _name="bank.account"

    name=fields.Char("Account Number")
    customer_id=fields.Many2one('customer.detail',string="Customer")
    balance=fields.Float("Balance")
    account_open_date=fields.Date("Opening Date")
    saving_account_type=fields.Selection(
        selection=[
            ('Saving', 'Saving'),
            ('Current', 'Current'),
                    ],
        string='Account Type',

    )
    business_name=fields.Char("Business Name")
    business_category=fields.Many2many(
        'customer.tag',string="Business Category" )

    def create(self, val):
        customer_id=val.get('customer_id',False)
        if customer_id:
            customer_id=self.env['customer.detail'].browse(customer_id)
            if not customer_id.is_kyc:
                raise UserError("Kyc is Not Completed")
        return super(BankAccount, self).create(val)










