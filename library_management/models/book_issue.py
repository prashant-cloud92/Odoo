from Tools.scripts.dutree import store

from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import timedelta

class StockMove(models.Model):
    _inherit = 'stock.move'

    is_returned = fields.Boolean(
        string="Returned",
        default=False
    )

class BookIssue(models.Model):
    _name = 'book.issue'
    _description = 'Book Issue'

    book_id = fields.Many2many("product.product",string="Book Name")
    member_id = fields.Many2one('res.users',string='Name')
    issue_date = fields.Date(string="Issue Date",default=fields.Date.today)
    return_date = fields.Date(string="Return Date",default=fields.Date.today)
    status = fields.Selection([('draft','Draft'),('issue','Issue'),('returned','Return')],default='draft', tracking=True,string="Status")
    days_issued = fields.Integer(compute='days_calculate',string="Days Issued",store=False)
    last_date = fields.Date(string="Last Date",default=fields.Date.today)
    total_penalty = fields.Float(string="Total Penalty",default=0)

    def create(self,vals):

        #vals['status'] = 'issue'



        record = super().create(vals)




        record.member_id.active = True
        record.book_id.available_qty=10
        for new_record in record.book_id:
            if new_record.id:
                if new_record.available_qty <= 0:
                    raise UserError("Book is not available!")

                #new_record.book_id.write({'available_qty':new_record.book_id.available_qty -1})
        return record

    @api.depends('issue_date','return_date')
    def days_calculate(self):
        for rec in self:
            rec.days_issued=0
            if rec.issue_date and rec.return_date:
                diff=(rec.return_date - rec.issue_date).days + 1
                rec.days_issued=diff


    def action_issue(self):

        picking_pool=self.env['stock.picking']
        picking_type_out = self.env.company.type_out
        #picking_type=self.env['stock.picking.type'].search([('name','=',"Delivery Orders")],limit=1,order='id')

        picking_id=picking_pool.create({'picking_type_id':picking_type_out.id if picking_type_out else False,
                                        'origin':f"issue ID : {self.id}"})

        for record in self.book_id:
            move_id=self.env['stock.move'].create({
                'product_id': record.id,
                'product_uom_qty':1,
                'location_id':picking_type_out.default_location_src_id.id,
                'location_dest_id':picking_type_out.default_location_dest_id.id,
                'name':'Product Move',
                'picking_id':picking_id.id
            })
        picking_id.action_confirm()
        picking_id.button_validate()
        self.status="issue"
        # for record in move_id:
        #     record.picking_id.button_validate()
        return

        # res_company_obj = self.env.company
        # for rec in self:
        #     if rec.book_id.available_qty <= 0:
        #         raise UserError("Book is not available!")
        #     rec.book_id.write({'available_qty':rec.book_id.available_qty -1})
        #     rec.write({'status':'issue'})
        #     rec.last_date=self.issue_date + timedelta(days=res_company_obj.book_validity)
        #     rec.write({'last_date':rec.last_date})



        # all_record_line=[]
        # for item in vals["line_ids"]:
        #     if item[0]==0:
        #         data=item[2]
        #         all_record_line.append(data)
        #
        # all_record_line=sorted(all_record_line,key=lambda x:x.get('from_days',0))
        #
        # for i in range(len(all_record_line)-1):
        #     if all_record_line[i]['to_days']>=all_record_line[i+1]['from_days']:
        #         raise UserError("Range Overlapping")
        #     if all_record_line[i]['to_days']==all_record_line[i]['from_days']:
        #         raise UserError("From date and To date Same not allowed")

    class MyWizardLine(models.TransientModel):
        _name = 'my.wizard.line'

        wizard_id = fields.Many2one('my.wizard.return')

        selected = fields.Boolean()
        move_id = fields.Many2one(
            'stock.move'
        )

        product_id = fields.Many2one('product.product')
        qty = fields.Float()
    class MyWizard(models.TransientModel):
        _name = 'my.wizard.return'
        _description = 'My Wizard'

        main_id = fields.Many2one('book.issue', string="Main Record")

        line_ids = fields.One2many(
            'my.wizard.line',
            'wizard_id',
            string="Related Records"
        )

        def action_return_picking(self):


            picking_id= self.main_id
            # picking_type_out=self.env.ref('stock.picking_type_out')
            # picking_type_in = self.env.ref('stock.picking_type_in')
            picking_type_out = self.env.company.type_out
            picking_type_in = self.env.company.type_in

            return_picking=self.env['stock.picking'].create({
                'picking_type_id':picking_type_in.id,

                'location_id':picking_type_in.default_location_src_id.id,
                'location_dest_id':picking_type_in.default_location_dest_id.id,
                'origin':f"issue ID : {self.main_id.id}",
            })

            if any(line.selected for line in self.line_ids):


                for line in self.line_ids:

                    original_move = line.move_id
                    if line.qty > 0:

                        move_id = self.env['stock.move'].create({
                            'product_id': line.product_id.id,
                            'product_uom_qty': 1,
                            'location_id': picking_type_in.default_location_src_id.id,
                            'location_dest_id': picking_type_in.default_location_dest_id.id,
                            'name': 'Product Move',
                            'picking_id': return_picking.id
                        })

                        original_move.is_returned = True
            else:
                raise UserError("Please Select at least one Book")

            return_picking.action_confirm()
            return_picking.action_assign()
            return_picking.button_validate()
            self.main_id.status = "returned"

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'res_id': return_picking.id,
                'view_mode': 'form',
            }


        @api.model
        def default_get(self, fields_list):
            res = super().default_get(fields_list)

            main_id = self.env.context.get('default_main_id')

            if main_id:
                lines = []
                pickings = self.env['stock.picking'].search([
                    ('origin', '=', f"issue ID : {main_id}"),
                    ('state', '=', 'done'),

                ])
                moves = self.env['stock.move'].search([('picking_id', 'in', pickings.ids)])
                for move in moves:
                    if move.is_returned:
                        continue

                    lines.append((0, 0, {
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'qty': 1,
                    }))

                res['line_ids'] = lines

            return res


    def action_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Wizard',
            'res_model': 'my.wizard.return',
            'view_mode': 'form',
            'target': 'new',  # open popup
            'context': {
                'default_main_id': self.id,  # pass current record id
            }
        }
        # res_company_obj = self.env.company
        # for record in self:
        #
        #     panalty_charge = res_company_obj.penalty_charge
        #
        #     book_validity =res_company_obj.book_validity
        #
        #     last_date=record.last_date
        #     final_penalty = 0
        #
        #
        #     if not self.return_date:
        #         raise UserError("Please Select Return Date")
        #     delay_days = (self.return_date - last_date).days
        #
        #     if delay_days:
        #
        #         if delay_days > book_validity:
        #             if delay_days > (book_validity * 2):
        #                 final_penalty=panalty_charge * 2
        #             else:
        #                 company = self.env['custom.penalty'].search([('from_days', '<=', delay_days),
        #                                                             ('to_days', '>=', delay_days),('company_id', '=', self.env.company.id)])
        #                 final_penalty=panalty_charge + (panalty_charge * company.penalty_charge/100)
                    #not dynamic
                    # if 10 < delay_days < 20:
                    #     final_penalty = 100 + ((10 / 100) * 100)
                    # elif 20 < delay_days < 30:
                    #     final_penalty = 100 + ((20 / 100) * 100)
                    # elif 30 < delay_days < 40:
                    #     final_penalty = 100 + ((30 / 100) * 100)
                    # else:
                    #     final_penalty = 100 + ((100 / 100) * 100)

            # record.total_penalty = final_penalty
            #
            # record.book_id.write({'available_qty': record.book_id.available_qty + 1})
            # record.write({'status': 'returned', 'return_date': self.return_date})



    def open_calender_field(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Book',
            'res_model': 'date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_issue_book_id': self.id
            }
        }



class DateWizard(models.TransientModel):
    _name = 'date.wizard'

    issue_book_id=fields.Many2one('book.issue',string="Book Name")
    return_date = fields.Date(string="Return Date", default=fields.Date.today,required=True)



    def action_confirm_return(self):
        record=self.issue_book_id



        record.return_date=self.return_date








    # def action_return(self):
    #     for rec in self:
    #         rec.status = 'return'
    #
    # def action_submit(self):
    #     for rec in self:
    #         rec.status = 'issue'
    #
    # def action_reset(self):
    #     for rec in self:
    #         rec.status = 'draft'