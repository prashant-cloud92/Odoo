from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

class CustomPenalty(models.Model):

    _name = 'custom.penalty'

    from_days = fields.Integer(string="From Days")
    to_days = fields.Integer(string="To Days")
    penalty_charge=fields.Integer(string="Penalty Charge (%)")
    company_id = fields.Many2one(comodel_name='res.company', string="Company")

    def create(self, vals):
        records = self.search([
            ('company_id', '=', self.env.company.id)
        ])

        fetch_data=[]
        for record in records.read(['from_days','to_days']):
            temp={'from_days':record['from_days'],
                  'to_days':record['to_days']}
            fetch_data.append(temp)

        all_record_new_fetch=fetch_data + vals

        for record in all_record_new_fetch:
            if record['from_days'] > record['to_days']:
                raise ValidationError("from days not greater than to days")
            if record['to_days'] == record['from_days']:
                raise ValidationError("from days and to days not equal valid")

        all_record_new_fetch=sorted(all_record_new_fetch,key=lambda x:x['from_days'])
        if len(all_record_new_fetch)>1:
            for i in range(len(all_record_new_fetch)-1):
                if all_record_new_fetch[i]['to_days'] >= all_record_new_fetch[i+1]['from_days']:
                    raise ValidationError("Range Overlapping")




        return super(CustomPenalty, self).create(vals)

