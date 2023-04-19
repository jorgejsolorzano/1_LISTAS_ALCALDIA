# -*- coding: utf-8 -*-
# from odoo import http


# class Herencias(http.Controller):
#     @http.route('/herencias/herencias', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/herencias/herencias/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('herencias.listing', {
#             'root': '/herencias/herencias',
#             'objects': http.request.env['herencias.herencias'].search([]),
#         })

#     @http.route('/herencias/herencias/objects/<model("herencias.herencias"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('herencias.object', {
#             'object': obj
#         })
