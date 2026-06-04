# -*- coding: utf-8 -*-
# from odoo import http


# class CsvImport(http.Controller):
#     @http.route('/csv_import/csv_import', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/csv_import/csv_import/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('csv_import.listing', {
#             'root': '/csv_import/csv_import',
#             'objects': http.request.env['csv_import.csv_import'].search([]),
#         })

#     @http.route('/csv_import/csv_import/objects/<model("csv_import.csv_import"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('csv_import.object', {
#             'object': obj
#         })

