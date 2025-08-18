# -*- coding: utf-8 -*-
# Part of Marlon Falcon. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import random

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_password = fields.Char('Attendance Password')
    last_password_update = fields.Datetime('Last Password Update')
    active_login = fields.Boolean('Active Login', default=True)
    token = fields.Char('Token')

    def generate_token(self):
        random_token = random.randint(1000000000, 20000000000)
        self.token = str(random_token)

    @api.onchange('attendance_password')
    def _onchange_attendance_password(self):
        self.last_password_update = fields.Datetime.now()

    def action_crate_password(self):
        random_password = random.randint(100000, 200000)
        self.attendance_password = str(random_password)
        self.last_password_update = fields.Datetime.now()