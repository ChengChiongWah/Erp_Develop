# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WahTestCourse(models.Model):
    _name = 'wah.test.course'

    name = fields.Char('Name')
    student_id = fields.Many2many('wah.test.student', 'student_teacher', 'student_id', 'teacher_id', string="StudentId")
    teacher_id = fields.Many2one('wah.test.teacher', string='TeacherId')

    def begin_course(self):
        pass