from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

class CustomPenalty(models.Model):

    _name = 'custom.penalty'

    from_days = fields.Integer(string="From Days")
    to_days = fields.Integer(string="To Days")
    penalty_charge=fields.Integer(string="Penalty Charge (%)")
    company_id = fields.Many2one(comodel_name='res.company', string="Company")


    @api.constrains('from_days', 'to_days')
    def range_overlapping_cheker(self):




        for rec in self:

            if rec.from_days >= rec.to_days:
                raise ValidationError("From Date not Greater or Equal to To Days")
            records=self.search([
            ('company_id', '=', rec.company_id.id),
            ('id', '!=', rec.id)
            ])

            for r in records:

                if rec.from_days <= r.to_days and rec.to_days >= r.from_days:
                    raise ValidationError("Range overlap detected")


            # if any(
            #         rec.from_days <= r.to_days and rec.to_days >= r.from_days
            #         for r in records
            # ):
            #     raise ValidationError("Range overlapping detected!")

        # this for argument in function
        # for new in new_data:
        #     if any(new[0] <= old[1] and new[1] >= old[0] for old in old_record):
        #         return True
        #
        #
        #
        # if any(
        #         i != j and r1[0] <= r2[1] and r1[1] >= r2[0]
        #         for i, r1 in enumerate(new_data)
        #         for j, r2 in enumerate(new_data)
        # ):
        #     return True
        # return False



    # def create(self, vals):
    #
    #
    #     records = self.search([
    #         ('company_id', '=', self.env.company.id)
    #     ])
    #
    #     old_record=records.mapped(lambda x:(x.from_days,x.to_days))
    #     new_data=[(fd.get("from_days"),fd.get("to_days")) for fd in vals]
    #
    #     if self.range_overlapping_cheker(old_record,new_data):
    #         raise ValidationError("Overlapping Found")
    #
    #     return super(CustomPenalty, self).create(vals)
    #
    # def write(self, vals):
    #
    #     records = self.search([
    #         ('company_id', '=', self.env.company.id),
    #         ('id', 'not in', self.ids)
    #     ])
    #
    #     old_record = records.mapped(lambda x: (x.from_days, x.to_days))
    #
    #     new_data = []
    #
    #     for rec in self:
    #         from_days = vals.get('from_days', rec.from_days)
    #         to_days = vals.get('to_days', rec.to_days)
    #
    #         new_data.append((from_days, to_days))
    #
    #     if self.range_overlapping_cheker(old_record, new_data):
    #         raise ValidationError("Overlapping Found")
    #
    #     return super(CustomPenalty, self).write(vals)
        # fetch_data=[]
        # for record in records.read(['from_days','to_days']):
        #     temp={'from_days':record['from_days'],
        #           'to_days':record['to_days']}
        #     fetch_data.append(temp)
        #
        # all_record_new_fetch=fetch_data + vals
        #
        # for record in all_record_new_fetch:
        #     if record['from_days'] > record['to_days']:
        #         raise ValidationError("from days not greater than to days")
        #     if record['to_days'] == record['from_days']:
        #         raise ValidationError("from days and to days not equal valid")
        #
        # all_record_new_fetch=sorted(all_record_new_fetch,key=lambda x:x['from_days'])
        # if len(all_record_new_fetch)>1:
        #     for i in range(len(all_record_new_fetch)-1):
        #         if all_record_new_fetch[i]['to_days'] >= all_record_new_fetch[i+1]['from_days']:
        #             raise ValidationError("Range Overlapping")







        #return super(CustomPenalty).write(vals)

