# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WahTestStudent(models.Model):
    _name = 'wah.test.student'

    name = fields.Char('Name')
    age = fields.Integer('Age')