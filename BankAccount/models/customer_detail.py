from Tools.scripts.dutree import store

from odoo import api, fields, models, tools

class CustomerDetail(models.Model):
    _name = "customer.detail"
    _description = "Customer Detail"
    _rec_name = 'name'

    name = fields.Char("Customer Name")
    surname = fields.Char("Surname")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    village = fields.Char("Village")
    is_kyc = fields.Boolean("Is KYC",default=False)

    bank_account_number = fields.One2many('bank.account','customer_id',string="Customer")
    total_balance = fields.Float("Total Balance")
    total_balance_compute=fields.Float(compute="calculate_total_balance",string="Total Balance Compute",store=True)

    @api.depends('bank_account_number','bank_account_number.balance','bank_account_number.customer_id')
    def calculate_total_balance(self):
        balance=0
        for rec in self:
            for acc in rec.bank_account_number:
                balance+=acc.balance
            rec.total_balance_compute=balance

    def write(self, vals):
        #here self in current object and val in edited field write method override
        # Check field
        rec=super().write(vals)
        if 'is_kyc' in vals:

                bank_id=self.bank_account_number
                for account_id in bank_id:
                    account_id.write({'is_active':vals['is_kyc']})

#bank_acc_ids.write({'is_active':vals['is_kyc']}) #Option 2
        return rec
