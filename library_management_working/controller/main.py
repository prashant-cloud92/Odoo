from fastapi import FastAPI
import xmlrpc.client
from odoo import http
from odoo.http import request
import json


# app = FastAPI()
#
# url = "http://127.0.0.1:8069"
# db = "odoo18"
# username = "admin"
# password = "admin"
#
# common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
# uid = common.authenticate(db, username, password, {})
#
# models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
#
#
# @app.get("/books")
# def get_books():
#
#     books = models.execute_kw(
#         db,
#         uid,
#         password,
#         'book.issue',
#         'search_read',
#         [[]],
#         {
#             'fields': ['status']
#         }
#     )
#
#     return books

class BookAPI(http.Controller):

    @http.route(
        '/api/book/create',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def create_book(self, **kwargs):
        token = request.httprequest.headers.get('api-key')

        if token != 'kalavadiya12':
            return {
                'status': 'error',
                'message': 'Invalid API Key'
            }

        data = request.httprequest.get_json()


        book = request.env['book.detail'].sudo().create({
            'name': data.get('name'),
            'author_name': data.get('author'),
            'available_qty': data.get('Qty'),
        })

        return {
            'status': 'success',
            'book_id': book.id,
            'message': 'Book Created'
        }

    @http.route(
        '/api/book/update',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def update_book(self, **kwargs):

        # API Key Validation
        token = request.httprequest.headers.get('api-key')

        if token != 'kalavadiya12':
            return {
                'status': 'error',
                'message': 'Invalid API Key'
            }

        data = request.httprequest.get_json()

        # Search Record
        book = request.env['book.detail'].sudo().browse(data.get('id'))

        # Check record exists
        if not book.exists():
            return {
                'status': 'error',
                'message': 'Book Not Found'
            }

        # Update Record
        book.write({
            'name': data.get('name'),
            'author_name': data.get('author'),

        })

        return {
            'status': 'success',
            'message': 'Book Updated Successfully'
        }