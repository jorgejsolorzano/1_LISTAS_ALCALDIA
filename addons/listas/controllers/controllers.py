# -*- coding: utf-8 -*-
# from odoo import http


# class Listas(http.Controller):
#     @http.route('/listas/listas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/listas/listas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('listas.listing', {
#             'root': '/listas/listas',
#             'objects': http.request.env['listas.listas'].search([]),
#         })

#     @http.route('/listas/listas/objects/<model("listas.listas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('listas.object', {
#             'object': obj
#         })
