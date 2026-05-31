#res = requests.post("http://localhost:8018/list_of_books",json={}) for read json

import json
from odoo import http
from odoo.http import request

class library_management(http.Controller):

    @http.route(['/list_of_books'],method=['POST'],csrf=False,type='json',auth='public')
    def list_of_books(self):
        book_data={}
        books=request.env['book.issue'].sudo().search([])
        for book in books:
            book_data[book.id] = {'status': book.status, 'member_id': book.member_id}
        return book_data
