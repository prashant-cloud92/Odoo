from logging import exception

from Tools.scripts.dutree import store

from odoo import models,fields,api
from odoo.exceptions import UserError
from odoo.exceptions import UserError


class BankAccount(models.Model):
    _name="bank.account"

    name=fields.Char("Account Number")
    customer_id=fields.Many2one('customer.detail',string="Customer")
    balance=fields.Float("Balance")
    total_balance=fields.Float(compute='total_balance_compute',string="Total Balance",store=True)
    account_open_date=fields.Date("Opening Date")
    saving_account_type=fields.Selection(
        selection=[
            ('Saving', 'Saving'),
            ('Current', 'Current'),
                    ],
        string='Account Type',

    )
    status=fields.Boolean("Account Status",default=False)
    business_name=fields.Char("Business Name")
    business_category=fields.Many2many(
        'customer.tag',string="Business Category" )
    acc_transaction_ids=fields.One2many("account.transaction","bank_account_id")
    is_active=fields.Boolean("Is Active",default=True)
    is_active_kyc=fields.Boolean(compute='_compute_is_active_kyc',string="KYC Status")


    def _compute_is_active_kyc(self):
        for rec in self:
            is_kyc = False

            for data in rec.customer_id:
                if data.adhar_numer and data.mob_number and data.pan_number:
                    is_kyc=True
            rec.is_active_kyc=is_kyc


    @api.depends('acc_transaction_ids','acc_transaction_ids.bank_account_id','acc_transaction_ids.amount','acc_transaction_ids.transaction_type')

    def total_balance_compute(self):


        for record in self:
            # acc_transaction_fetch = record.env['account.transaction']
            # acc_transaction_id = acc_transaction_fetch.search([('bank_account_id', '=', record.id)])
            balance=0
            # if acc_transaction_id:
            for transaction in record.acc_transaction_ids:
                if transaction.transaction_type=="credit":
                    balance+=transaction.amount
                else:
                    balance-=transaction.amount
            # else:
            #     raise UserError("no found record")

            record.total_balance=balance






    def create(self, val):
        customer_id=val.get('customer_id',False)
        if customer_id:
            customer_id=self.env['customer.detail'].browse(customer_id)
            if not customer_id.is_kyc:
                raise UserError("Kyc is Not Completed")
        return super(BankAccount, self).create(val)

    @api.depends('name','customer_id.name')
    def _compute_display_name(self):
        super()._compute_display_name()

        for rec in self:
            customer=rec.customer_id.name or ''
            rec.display_name = f"{rec.display_name} - {customer}"
# def create(self,vals):
#     return super(BalanceTransfer,self).create(vals)
#
# def write(self,vals):
#     self.from_acc_id
#     return super(BalanceTransfer,self).write(vals)










