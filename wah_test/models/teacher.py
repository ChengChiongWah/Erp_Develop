# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WahTestTeacher(models.Model):
    _name = 'wah.test.teacher'

    name = fields.Char('Name')
    course_id = fields.One2many('wah.test.course', 'teacher_id', string='CourseId')
