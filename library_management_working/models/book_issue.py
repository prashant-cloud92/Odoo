from typing_extensions import Self

from odoo import fields,models,api
from datetime import datetime, timedelta

from odoo.addons.test_convert.tests.test_env import record
from odoo.api import ValuesType
from odoo.exceptions import ValidationError


class BookIssue(models.Model):
    _name = 'book.issue'
    _description = 'Book Detail'
    _rec_name = 'sequence_gen'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence_gen = fields.Char(string="Issue No", readonly=True,
                               default="New")
    member_id = fields.Many2one('res.users',string='Name')
    status = fields.Selection(
        [('draft', 'Draft'), ('issue', 'Issue'), ('returned_partially', 'Partially Return'), ('returned', 'Return')],
        default='draft', tracking=True, string="Status")
    total_penalty = fields.Float(string="Total Penalty", default=0)
    last_date = fields.Date(string="Last Date", default=fields.Date.today)
    line_ids = fields.One2many(
        'library.issue.line',
        'issue_id',
        string='Books'
    )

    remaining_line_ids = fields.One2many(
        'library.issue.line',
        'issue_id',
        domain=[('is_return', '=', False)]
    )

    def create(self, vals):
        # vals['status'] = 'issue'

        if vals.get('sequence_gen', 'New') == 'New':
            vals['sequence_gen'] = self.env['ir.sequence'].next_by_code(
                'book.issue'
            ) or 'New'
        return super().create(vals)

    @api.constrains('line_ids')
    def _check_stock(self):

        for rec in self:
            books = []
            for line in rec.line_ids:

                if line.qty > line.book_id.available_qty:
                    raise ValidationError(
                        f"Not enough stock for {line.book_id.name}"
                    )
                if line.qty <= 0:
                    raise ValidationError("Qty must be greater than 0.")


                books.append(line.book_id.id)

            if len(books) != len(set(books)):
                raise ValidationError("Same book selected multiple times.")

    def action_issue(self):
        picking_pool = self.env['stock.picking']
        picking_type_out = self.env.company.type_out


        for rec in self:

            if not rec.line_ids:
                raise ValidationError(
                    "Please add books."
                )

            picking_id = picking_pool.create({'picking_type_id': picking_type_out.id if picking_type_out else False,
                                              'origin': f"issue ID : {rec.id}"})
            for line in rec.line_ids:

                line.book_id.available_qty -= line.qty
                product = line.book_id.product_id

                if not product:
                    raise ValidationError(
                        f"Product missing in {line.book_id.name}"
                    )

                self.env['stock.move'].create({
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': line.qty,

                    'picking_id': picking_id.id,
                    'location_id': picking_type_out.default_location_src_id.id,
                    'location_dest_id': picking_type_out.default_location_dest_id.id,
                })
            picking_id.action_confirm()
            picking_id.action_assign()

            picking_id.button_validate()

            rec.status = 'issue'

    def action_return(self):
        picking_pool = self.env['stock.picking']
        picking_type_in = self.env.company.type_in

        for rec in self:

            selected_lines = rec.line_ids.filtered(
                lambda l: l.return_select
            )
            total_lines = len(rec.line_ids)
            remaining_lines = rec.line_ids.filtered(
                lambda l: not l.is_return
            )


            picking_id = picking_pool.create({
                'picking_type_id': picking_type_in.id,
                'origin': f"Return ID : {rec.id}"
            })
            rec.total_penalty = 0
            for line in selected_lines:
                product = line.book_id.product_id

                line.is_return = True
                line.return_select = False

                self.env['stock.move'].create({
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': line.qty,
                    'picking_id': picking_id.id,
                    'location_id': picking_type_in.default_location_src_id.id,
                    'location_dest_id': picking_type_in.default_location_dest_id.id,
                })

                line.book_id.available_qty += line.qty


                line.penalty_sigle_book = 0

                if line.return_date > line.last_date:
                    late_days = (
                            line.return_date - line.last_date
                    ).days

                    if late_days > 10:
                        line.penalty_sigle_book = late_days * 10
                        rec.total_penalty+=late_days * 10



            picking_id.action_confirm()
            picking_id.action_assign()
            picking_id.button_validate()






            if len(selected_lines) == len(remaining_lines):
                rec.status = 'returned'
            else:
                rec.status = 'returned_partially'



    def action_return_partially(self):
        picking_pool = self.env['stock.picking']
        picking_type_in = self.env.company.type_in

        for rec in self:

            selected_lines = rec.line_ids.filtered(
                lambda l: l.return_select
            )
            total_lines = len(rec.line_ids)
            remaining_lines = rec.line_ids.filtered(
                lambda l: not l.is_return
            )
            picking_id = picking_pool.create({
                'picking_type_id': picking_type_in.id,
                'origin': f"Return ID : {rec.id}"
            })

            for line in selected_lines:
                product = line.book_id.product_id


                line.is_return = True
                line.return_select = False
                self.env['stock.move'].create({
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': line.qty,
                    'picking_id': picking_id.id,
                    'location_id': picking_type_in.default_location_src_id.id,
                    'location_dest_id': picking_type_in.default_location_dest_id.id,
                })

                line.book_id.available_qty += line.qty

            picking_id.action_confirm()
            picking_id.action_assign()
            picking_id.button_validate()

            if len(selected_lines) == len(remaining_lines):
                rec.status = 'returned'

                rec.total_penalty = 0

                for line in rec.line_ids:

                    if line.return_date > line.last_date:
                        late_days = (
                                line.return_date - line.last_date
                        ).days

                        if late_days > 10:

                            line.penalty_sigle_book = late_days * 10

            else:
                rec.status = 'returned_partially'




class LibraryIssueLine(models.Model):
    _name = 'library.issue.line'
    _description = 'Library Issue Line'

    issue_id = fields.Many2one(
        'book.issue',
        string='Issue'
    )
    return_select = fields.Boolean(
        string='Return'
    )

    is_return = fields.Boolean(
        string='Returned',
        default=False)

    book_id = fields.Many2one('book.detail',string='Books',required=True)


    qty = fields.Integer("Qty")

    issue_date = fields.Date("Issue Date", default=fields.Date.today)
    last_date = fields.Date("Last Date", default=fields.Date.today)
    return_date = fields.Date("Return Date", default=fields.Date.today)
    penalty_sigle_book = fields.Float("Penalty")



    @api.onchange('issue_date')
    def onchange_issue_date(self):
     for record in self:
         record.last_date = record.issue_date + timedelta(days=10)

    @api.onchange('book_id')
    def onchange_book_id(self):
        for record in self:
            record.qty=1

    @api.constrains('qty')
    def _check_qty(self):

        for line in self:

            # Issue time
            if line.issue_id.status == 'draft':

                if line.qty <= 0:
                    raise ValidationError(
                        "Qty must be greater than zero."
                    )

            # Return time
            else:

                if line.return_select and line.qty <= 0:
                    raise ValidationError(
                        "Return qty must be greater than zero."
                    )