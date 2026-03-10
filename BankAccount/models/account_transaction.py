from odoo import api, fields, models, tools
class AccountTransaction(models.Model):
    _name = 'account.transaction'

    _description = 'Account Transaction'

    bank_account_id = fields.Many2one('bank.account','Bank Account')
    customer_id = fields.Many2one('customer.detail','Customer')
    amount = fields.Float('Amount')
    date = fields.Date("Date",default=lambda self:fields.Date.context_today(self))
    transaction_type = fields.Selection([('credit', 'Credit'),
                                        ('debit','Debit')],
                                        'Transaction Type')
    customer_ids = fields.Many2one('customer.detail',related='bank_account_id.customer_id')

    @api.onchange('bank_account_id')
    def _onchange_bank_account_id(self):
        #self.customer_id=self.bank_account_id and self.bank_account_id.customer_id.id or False
        customer_id = False
        if self.bank_account_id:

            customer_id=self.bank_account_id.customer_id.id
        self.customer_id = customer_id
