# -*- coding: utf-8 -*-
from odoo import http

# class WahTest(http.Controller):
#     @http.route('/wah_test/wah_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wah_test/wah_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wah_test.listing', {
#             'root': '/wah_test/wah_test',
#             'objects': http.request.env['wah_test.wah_test'].search([]),
#         })

#     @http.route('/wah_test/wah_test/objects/<model("wah_test.wah_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wah_test.object', {
#             'object': obj
#         })