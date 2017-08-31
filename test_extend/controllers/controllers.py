# -*- coding: utf-8 -*-
from odoo import http

# class TestExtend(http.Controller):
#     @http.route('/test_extend/test_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_extend/test_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_extend.listing', {
#             'root': '/test_extend/test_extend',
#             'objects': http.request.env['test_extend.test_extend'].search([]),
#         })

#     @http.route('/test_extend/test_extend/objects/<model("test_extend.test_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_extend.object', {
#             'object': obj
#         })