from odoo import fields, models
class SaleExtend(models.Model):
    _inherit = "sale.order"

    transport_name=fields.Char("Transport Name")
    product_in_details=fields.Char("Product Details")

    def pop_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order Wizard',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            #'view_id': self.env.ref('sale.order.wizard.view_my_popup_wizard_form').id,
            'context': {
                'active_id': self.id,
                'active_model': self._name,

            }
        }

class ClickMe(models.TransientModel):
    _name="sale.order.wizard"

    tax_select=fields.Char("Taxes")

    def submit_action(self):
        active_id=self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')

        record = self.env[active_model].browse(active_id)

        # Example use
        record.write({
            'tax_select': self.tax_select
        })

        return {'type': 'ir.actions.act_window_close'}
