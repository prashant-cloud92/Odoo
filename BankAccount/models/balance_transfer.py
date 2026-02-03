from odoo import api,fields,models,tools
from odoo.exceptions import UserError

class BalanceTransfer(models.Model):
    _name = 'balance.transfer'
    _description = 'Balance Transfer'


    from_account_id = fields.Many2one('bank.account',string='From Account')

    to_account_id = fields.Many2one('bank.account',string='To Account')

    amount = fields.Float("Amount")

    def balance_transfer_click(self):

        if self.amount<0 or self.amount==0:
            raise UserError("Please enter a positive amount")
        elif self.from_account_id.balance < self.amount:
            raise UserError("Insufficient balance")

        self.from_account_id.write({'balance':self.from_account_id.balance-self.amount})
        self.to_account_id.write({'balance':self.to_account_id.balance+self.amount})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Balance transferred successfully.',
                'type': 'success',
                'sticky': False,
            }
        }