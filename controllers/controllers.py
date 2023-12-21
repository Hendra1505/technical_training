# -*- coding: utf-8 -*-
# from odoo import http


# class TechnicalTrainingFcModule(http.Controller):
#     @http.route('/technical_training_fc_module/technical_training_fc_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/technical_training_fc_module/technical_training_fc_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('technical_training_fc_module.listing', {
#             'root': '/technical_training_fc_module/technical_training_fc_module',
#             'objects': http.request.env['technical_training_fc_module.technical_training_fc_module'].search([]),
#         })

#     @http.route('/technical_training_fc_module/technical_training_fc_module/objects/<model("technical_training_fc_module.technical_training_fc_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('technical_training_fc_module.object', {
#             'object': obj
#         })
