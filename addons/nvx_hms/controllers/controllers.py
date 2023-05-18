# -*- coding: utf-8 -*-
from odoo import http

# class NvxHms(http.Controller):
#     @http.route('/nvx_hms/nvx_hms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nvx_hms/nvx_hms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nvx_hms.listing', {
#             'root': '/nvx_hms/nvx_hms',
#             'objects': http.request.env['nvx_hms.nvx_hms'].search([]),
#         })

#     @http.route('/nvx_hms/nvx_hms/objects/<model("nvx_hms.nvx_hms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nvx_hms.object', {
#             'object': obj
#         })