# -*- coding: utf-8 -*-
# from odoo import http


# class Odoomoduleyes(http.Controller):
#     @http.route('/odoomoduleyes/odoomoduleyes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoomoduleyes/odoomoduleyes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoomoduleyes.listing', {
#             'root': '/odoomoduleyes/odoomoduleyes',
#             'objects': http.request.env['odoomoduleyes.odoomoduleyes'].search([]),
#         })

#     @http.route('/odoomoduleyes/odoomoduleyes/objects/<model("odoomoduleyes.odoomoduleyes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoomoduleyes.object', {
#             'object': obj
#         })
