# -*- coding: utf-8 -*-
# Part of Marlon Falcon. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    project_id = fields.Many2one('project.project', string='Project')