# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.modules.registry import Registry


class TestExtend(models.Model):
    _name = 'test.module.extend'

    module_name = fields.Many2one('ir.module.module', String='Module name')

    @api.model
    def begin_test_model(self):
        module_name1 = 'product_extend'
        dbname = 'user01'
        test_enable_val = odoo.tools.config['test_enable']
        if not test_enable_val:
            odoo.tools.config['test_enable'] = True
            if not odoo.tools.config['init']:
                odoo.tools.config['init'] = {module_name1: 1}
                test_result = Registry.new(db_name=dbname, force_demo=False, status=None, update_module={module_name1: 1})
                print odoo.tools.config['init']
                print 'haha', self.module_name
            odoo.tools.config['test_enable'] = False
        else:
            if not odoo.tools.config['init']:
                odoo.tools.config['init'] = {module_name1: 1}
                test_result = Registry.new(db_name=dbname, force_demo=False, status=None, update_module={module_name1: 1})
                print odoo.tools.config['init']
            print 'hehe'
